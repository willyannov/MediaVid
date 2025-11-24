import yt_dlp
from typing import Optional, Dict, Any
import os
import shutil
import subprocess
import re
import asyncio
import requests
import random
import string
import time
import tempfile
from pathlib import Path
from app.models.video import VideoInfo, VideoFormat, DownloadRequest
from app.utils.validators import detect_platform, sanitize_filename
from app.config import settings
from app.services.tiktok_fallback import TikTokFallback
from app.services.browser_cookies import BrowserCookieExtractor


class VideoDownloader:
    def __init__(self):
        self.temp_path = Path(settings.TEMP_DOWNLOAD_PATH)
        self.temp_path.mkdir(exist_ok=True)
        
        # Detecta FFmpeg
        self.ffmpeg_location = self._find_ffmpeg()
        
        # Referência ao manager de WebSocket (será injetada)
        self.ws_manager = None
        
        # Cache de informações de vídeo (evita requisições duplicadas)
        self._info_cache = {}
        
        # Fallback para TikTok
        self.tiktok_fallback = TikTokFallback()
        
        # Cookies do YouTube
        self.youtube_cookies_file = self._setup_youtube_cookies()
        
        # Rate limiting para YouTube (evita erro 429)
        self._youtube_last_request = 0
        self._youtube_min_interval = 3  # segundos entre requisições
    
    def _setup_youtube_cookies(self) -> Optional[str]:
        """
        Configura cookies do YouTube:
        1. Produção: Usa variável de ambiente YOUTUBE_COOKIES
        2. Desenvolvimento: Extrai do navegador automaticamente
        """
        # Verifica se está em produção com cookies configurados
        if settings.YOUTUBE_COOKIES:
            print("🍪 Usando cookies do YouTube de variável de ambiente...")
            try:
                # Salva cookies em arquivo temporário
                cookie_file = tempfile.NamedTemporaryFile(
                    mode='w',
                    suffix='.txt',
                    delete=False,
                    encoding='utf-8'
                )
                cookie_file.write(settings.YOUTUBE_COOKIES)
                cookie_file.close()
                print(f"✅ Cookies salvos em: {cookie_file.name}")
                return cookie_file.name
            except Exception as e:
                print(f"⚠️ Erro ao processar cookies: {e}")
                return None
        
        # Desenvolvimento: Tenta extrair do navegador
        try:
            cookie_extractor = BrowserCookieExtractor()
            return cookie_extractor.extract_youtube_cookies()
        except Exception as e:
            print(f"ℹ️ Cookies do navegador não disponíveis: {e}")
            return None
    
    def _generate_random_code(self, length=8) -> str:
        """Gera código aleatório alfanumérico"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    def _apply_youtube_rate_limit(self):
        """Aplica rate limiting para YouTube (evita erro 429)"""
        elapsed = time.time() - self._youtube_last_request
        if elapsed < self._youtube_min_interval:
            sleep_time = self._youtube_min_interval - elapsed
            print(f"⏱️ Rate limiting: aguardando {sleep_time:.1f}s...")
            time.sleep(sleep_time)
        self._youtube_last_request = time.time()
    
    def set_websocket_manager(self, manager):
        """Injeta o manager de WebSocket"""
        self.ws_manager = manager
    
    async def send_progress(self, client_id: Optional[str], stage: str, progress: int, message: str):
        """Envia progresso via WebSocket se disponível"""
        if self.ws_manager and client_id:
            try:
                await self.ws_manager.send_progress(client_id, {
                    'stage': stage,
                    'progress': progress,
                    'message': message
                })
            except Exception as e:
                print(f"Erro ao enviar progresso: {e}")
    
    def send_progress_sync(self, client_id: Optional[str], stage: str, progress: int, message: str):
        """Versão síncrona para send_progress - cria novo event loop se necessário"""
        if self.ws_manager and client_id:
            try:
                # Tenta pegar loop existente ou cria um novo
                try:
                    loop = asyncio.get_running_loop()
                    # Se já existe um loop rodando, agenda a coroutine
                    asyncio.create_task(self.send_progress(client_id, stage, progress, message))
                except RuntimeError:
                    # Não há loop rodando, executa diretamente
                    asyncio.run(self.send_progress(client_id, stage, progress, message))
            except Exception as e:
                print(f"Erro ao enviar progresso: {e}")
    
    def _find_ffmpeg(self) -> Optional[str]:
        """Encontra o FFmpeg no sistema"""
        # Verifica se está no PATH
        if shutil.which('ffmpeg'):
            return shutil.which('ffmpeg')
        
        # Procura em locais comuns - ordem de prioridade
        possible_paths = [
            r"C:\Users\willy\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0-full_build\bin\ffmpeg.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0-full_build\bin\ffmpeg.exe"),
            r"C:\Program Files\ShareX\ffmpeg.exe",
            r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
            r"C:\ffmpeg\bin\ffmpeg.exe",
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                print(f"FFmpeg encontrado em: {path}")
                return path
        
        print("FFmpeg não encontrado em nenhum local conhecido")
        return None
    
    def _get_extractor_args(self, platform: str) -> dict:
        """Retorna configurações específicas do extractor por plataforma"""
        configs = {
            'YouTube': {
                'youtube': {
                    'player_client': ['android', 'web'],  # Tenta Android primeiro, depois web
                    'skip': ['hls', 'dash'],  # Pula formatos complexos
                }
            },
            'Instagram': {
                'instagram': {
                    'api_domain': 'i.instagram.com',  # API alternativa mais rápida
                }
            },
            'TikTok': {
                'tiktok': {
                    'api_hostname': 'api16-normal-c-useast1a.tiktokv.com',  # API global
                    'webpage_download': True,  # Força download via webpage ao invés de API
                }
            },
            'Twitter': {
                'twitter': {
                    'api': ['graphql', 'legacy', 'syndication'],  # Tenta múltiplas APIs
                }
            },
            'Facebook': {},
            'Reddit': {
                'reddit': {
                    'ydl_opts': {
                        'merge_output_format': 'mp4'  # Força merge em MP4
                    }
                }
            }
        }
        
        return configs.get(platform, {})
    
    def _try_youtube_with_different_configs(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Tenta extrair informações do YouTube com yt-dlp.
        Usa rate limiting para evitar erro 429 (Too Many Requests).
        """
        
        # Aplica rate limiting antes de qualquer requisição
        self._apply_youtube_rate_limit()
        
        # Config base otimizada para produção
        base_config = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'socket_timeout': 60,
            'retries': 3,
            'sleep_interval': 5,  # Delay mínimo entre requisições
            'max_sleep_interval': 15,  # Delay máximo
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'skip': ['hls', 'dash', 'translated_subs'],
                }
            },
        }
        
        # Se temos cookies (desenvolvimento local), adiciona
        if self.youtube_cookies_file:
            print("🍪 Usando cookies do navegador...")
            base_config['cookiefile'] = self.youtube_cookies_file
        
        # Tenta extrair
        try:
            print("🔄 YouTube: Extraindo vídeo...")
            with yt_dlp.YoutubeDL(base_config) as ydl:  # type: ignore
                info = ydl.extract_info(url, download=False)
                if info:
                    print("✅ Vídeo extraído com sucesso!")
                    return info
        except Exception as e:
            error_msg = str(e).lower()
            print(f"❌ Erro ao extrair: {str(e)[:150]}")
            
            # Se é erro 429, informa sobre rate limiting
            if '429' in error_msg or 'too many requests' in error_msg:
                print("⚠️ Erro 429: Muitas requisições. Aguardando antes de tentar novamente...")
                time.sleep(30)  # Espera 30s em caso de 429
            
            return None
    
    def get_video_info(self, url: str) -> VideoInfo:
        """Extrai informações do vídeo sem baixar"""
        
        # Verifica cache
        if url in self._info_cache:
            print("✓ Informações do vídeo recuperadas do cache")
            return self._info_cache[url]
        
        platform = detect_platform(url)
        
        # FALLBACK TIKTOK: Tenta API alternativa primeiro
        if platform == 'TikTok':
            try:
                print("🎵 TikTok detectado - tentando API alternativa...")
                tiktok_info = self.tiktok_fallback.get_video_info(url)
                
                if tiktok_info:
                    print("✓ Vídeo do TikTok obtido via API alternativa!")
                    video_info = VideoInfo(
                        url=tiktok_info['url'],
                        title=tiktok_info.get('title', 'TikTok Video'),
                        description=tiktok_info.get('description'),
                        thumbnail=tiktok_info.get('thumbnail'),
                        duration=tiktok_info.get('duration', 0),
                        uploader=tiktok_info.get('uploader'),
                        view_count=tiktok_info.get('view_count'),
                        formats=[],  # TikTok tem apenas uma qualidade
                        platform='TikTok'
                    )
                    
                    # Guarda no cache
                    self._info_cache[url] = video_info
                    return video_info
                else:
                    print("⚠ API alternativa do TikTok falhou, tentando yt-dlp...")
            except Exception as e:
                print(f"⚠ Erro ao usar API alternativa TikTok: {e}")
                print("→ Tentando yt-dlp como fallback...")
        
        # ESTRATÉGIA ESPECIAL PARA YOUTUBE
        if platform == 'YouTube':
            # Usa yt-dlp em todos ambientes (local e produção)
            # mweb é o cliente recomendado que não precisa de PO Token
            info = self._try_youtube_with_different_configs(url)
            
            if not info:
                raise Exception("Não foi possível acessar este vídeo do YouTube. Verifique se o vídeo é público e tente novamente.")
        else:
            # Continua com yt-dlp para outras plataformas (incluindo Twitter)
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'skip_download': True,
                # Otimizações
                'socket_timeout': 30,
                'retries': 3,
                'ignoreerrors': False,
                # User-Agent moderno
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-us,en;q=0.5',
                    'Sec-Fetch-Mode': 'navigate',
                },
                # Configurações específicas por plataforma
                'extractor_args': self._get_extractor_args(platform)
            }
            
            # Configurações específicas para Instagram (mais permissivo)
            if platform == 'Instagram':
                ydl_opts['username'] = None  # Sem autenticação
                ydl_opts['password'] = None
                ydl_opts['cookiefile'] = None
                ydl_opts['nocheckcertificate'] = True
                # User-Agent mobile do Instagram (menos restritivo)
                ydl_opts['http_headers'] = {
                    'User-Agent': 'Instagram 76.0.0.15.395 Android (24/7.0; 640dpi; 1440x2560; samsung; SM-G930F; herolte; samsungexynos8890; en_US; 138226743)',
                    'Accept': '*/*',
                    'Accept-Language': 'en-US',
                }
            
            # Configurações específicas para TikTok (bypass login)
            if platform == 'TikTok':
                ydl_opts['http_headers'] = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                    'Referer': 'https://www.tiktok.com/'
                }
                # Tenta extrair sem cookies primeiro
                ydl_opts['nocheckcertificate'] = True
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type: ignore
                    info = ydl.extract_info(url, download=False)
                    
                    if not info:
                        raise Exception("Não foi possível extrair informações do vídeo")
            except Exception as e:
                error_msg = str(e)
                error_lower = error_msg.lower()
                
                # Mensagens genéricas e amigáveis (sem expor detalhes técnicos)
                if 'unsupported url' in error_lower:
                    raise Exception("URL não suportada. Verifique se o link está correto.")
                elif 'private video' in error_lower or 'this video is private' in error_lower:
                    raise Exception("Este vídeo é privado e não pode ser acessado.")
                elif 'video unavailable' in error_lower or 'has been removed' in error_lower or 'no video could be found' in error_lower:
                    raise Exception("Vídeo indisponível, removido ou não contém mídia para download.")
                elif 'sign in' in error_lower or 'login' in error_lower or 'cookies' in error_lower or 'bot' in error_lower or 'authentication' in error_lower:
                    # Mensagem genérica sem mencionar detalhes técnicos
                    if platform == 'Instagram':
                        raise Exception("Este conteúdo do Instagram não está acessível no momento. Tente outro vídeo público.")
                    elif platform == 'Twitter':
                        raise Exception("Este conteúdo do Twitter/X não está acessível no momento. Tente outro vídeo público.")
                    else:
                        raise Exception("Este vídeo requer autenticação ou não está disponível publicamente.")
                elif 'geo restricted' in error_lower or 'not available in your country' in error_lower:
                    raise Exception("Este vídeo tem restrição geográfica e não está disponível na sua região.")
                elif 'http error 429' in error_lower or 'too many requests' in error_lower:
                    raise Exception("Muitas requisições. Por favor, aguarde alguns minutos.")
                elif 'empty media response' in error_lower:
                    raise Exception("O conteúdo não está disponível ou requer login. Tente outro vídeo público.")
                elif 'http error 404' in error_lower:
                    raise Exception("Conteúdo não encontrado. Verifique se o link está correto.")
                else:
                    # Mensagem genérica sem expor stack trace do yt-dlp
                    raise Exception("Não foi possível acessar este vídeo. Verifique se o link está correto e o vídeo é público.")
        
        # Processa os formatos disponíveis
        formats = []
        if 'formats' in info and info['formats']:
            for fmt in info['formats']:
                # Filtra apenas formatos válidos
                if fmt.get('ext') and fmt.get('format_id'):
                    video_format = VideoFormat(
                        format_id=fmt.get('format_id', ''),
                        ext=fmt.get('ext', ''),
                        quality=fmt.get('format_note'),
                        resolution=fmt.get('resolution'),
                        filesize=fmt.get('filesize'),
                        format_note=fmt.get('format_note'),
                        fps=fmt.get('fps'),
                        vcodec=fmt.get('vcodec'),
                        acodec=fmt.get('acodec'),
                    )
                    formats.append(video_format)
        
        # Cria objeto VideoInfo
        thumbnail_url = info.get('thumbnail')
        
        # Para Instagram, usa proxy para evitar CORS
        if platform == 'Instagram' and thumbnail_url:
            from urllib.parse import quote
            thumbnail_url = f"http://localhost:8000/api/video/proxy-thumbnail?url={quote(thumbnail_url)}"
        
        video_info = VideoInfo(
            url=url,
            title=info.get('title') or 'Unknown',
            description=info.get('description'),
            thumbnail=thumbnail_url,
            duration=info.get('duration'),
            uploader=info.get('uploader') or info.get('channel') or info.get('uploader_id'),
            uploader_url=info.get('uploader_url') or info.get('channel_url'),
            view_count=info.get('view_count'),
            formats=formats[:50] if len(formats) > 50 else formats,  # Limita a 50 formatos
            platform=platform
        )
        
        # Guarda no cache (expira automaticamente quando reiniciar o servidor)
        self._info_cache[url] = video_info
        
        return video_info
    
    def download_video(self, request: DownloadRequest) -> Dict[str, Any]:
        """Baixa o vídeo em MP4 ou áudio em MP3"""
        
        print(f"\n{'='*60}")
        print(f"DOWNLOAD INICIADO")
        print(f"URL: {request.url}")
        print(f"Qualidade: {request.quality}")
        print(f"Formato: {'MP3 (áudio)' if request.audio_only else 'MP4 (vídeo)'}")
        print(f"Client ID: {request.client_id}")
        print(f"{'='*60}\n")
        
        platform = detect_platform(request.url)
        
        # FALLBACK TIKTOK: Download direto via API alternativa
        if platform == 'TikTok' and not request.audio_only:
            try:
                print("🎵 TikTok detectado - usando download direto...")
                tiktok_info = self.tiktok_fallback.get_video_info(request.url)
                
                if tiktok_info and tiktok_info.get('download_url'):
                    if request.client_id and self.ws_manager:
                        self.send_progress_sync(
                            request.client_id, 'starting', 0, 'Iniciando download via API alternativa...'
                        )
                    
                    # Gera nome do arquivo: MediaVid{Plataforma}{CodigoAleatorio}.mp4
                    random_code = self._generate_random_code(8)
                    filename = f"MediaVidTikTok{random_code}.mp4"
                    filepath = self.temp_path / filename
                    
                    # Download direto
                    response = requests.get(tiktok_info['download_url'], stream=True, timeout=30)
                    if response.status_code == 200:
                        total_size = int(response.headers.get('content-length', 0))
                        downloaded = 0
                        
                        with open(filepath, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                                    downloaded += len(chunk)
                                    
                                    # Atualiza progresso
                                    if total_size > 0 and request.client_id and self.ws_manager:
                                        progress = int((downloaded / total_size) * 100)
                                        self.send_progress_sync(
                                            request.client_id,
                                            'downloading',
                                            progress,
                                            f'Baixando: {progress}%'
                                        )
                        
                        print(f"✓ TikTok baixado com sucesso via API alternativa!")
                        print(f"✓ Arquivo: {filepath.name}")
                        
                        if request.client_id and self.ws_manager:
                            self.send_progress_sync(
                                request.client_id, 'complete', 100, 'Pronto para download!'
                            )
                        
                        return {
                            'success': True,
                            'filename': filepath.name,
                            'filepath': str(filepath),
                            'title': tiktok_info.get('title'),
                            'filesize': os.path.getsize(filepath) if filepath.exists() else None
                        }
            except Exception as e:
                print(f"⚠ Falha no download direto do TikTok: {e}")
                print("→ Tentando yt-dlp como fallback...")
        
        # Variável para capturar o caminho do arquivo baixado
        downloaded_file_path = None
        
        # Hook de progresso para yt-dlp
        def progress_hook(d):
            nonlocal downloaded_file_path
            
            if d['status'] == 'downloading' and request.client_id:
                try:
                    percent_str = d.get('_percent_str', '0%').strip().replace('%', '')
                    try:
                        progress = int(float(percent_str))
                    except:
                        progress = 0
                    
                    speed = d.get('_speed_str', 'N/A')
                    eta = d.get('_eta_str', 'N/A')
                    
                    if self.ws_manager:
                        self.send_progress_sync(
                            request.client_id,
                            'downloading',
                            progress,
                            f'Baixando: {progress}% | Velocidade: {speed} | ETA: {eta}'
                        )
                except Exception as e:
                    print(f"Erro no progress_hook: {e}")
            
            elif d['status'] == 'finished':
                # Captura o caminho real do arquivo baixado
                downloaded_file_path = d.get('filename')
        
        # Gera nome do arquivo: MediaVid{Plataforma}{CodigoAleatorio}.{ext}
        random_code = self._generate_random_code(8)
        filename_template = f'MediaVid{platform}{random_code}.%(ext)s'
        
        # Configuração baseada no tipo - OTIMIZADA
        ydl_opts = {
            'quiet': True,  # Silencioso para não atrasar
            'no_warnings': True,
            'ignoreerrors': False,
            'noprogress': False,
            'outtmpl': str(self.temp_path / filename_template),
            'progress_hooks': [progress_hook],
            # Otimizações de velocidade máxima
            'concurrent_fragment_downloads': 10,  # Aumentado para 10 downloads paralelos
            'retries': 10,
            'fragment_retries': 10,
            'skip_unavailable_fragments': True,
            'http_chunk_size': 10485760,  # 10MB chunks
            'buffersize': 16384,  # Buffer de leitura 16KB
            'socket_timeout': 30,
            # Configurações específicas por plataforma
            'extractor_args': self._get_extractor_args(platform)
        }
        
        # Configurações específicas para Instagram no download também
        if platform == 'Instagram':
            ydl_opts['username'] = None
            ydl_opts['password'] = None
            ydl_opts['cookiefile'] = None
            ydl_opts['http_headers'] = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
            }
        
        # Configurações específicas para TikTok no download também
        if platform == 'TikTok':
            ydl_opts['http_headers'] = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                'Referer': 'https://www.tiktok.com/'
            }
            ydl_opts['nocheckcertificate'] = True
        
        # Configurações específicas para Reddit - desabilita downloads fragmentados problemáticos
        if platform == 'Reddit':
            ydl_opts['concurrent_fragment_downloads'] = 1  # Apenas 1 fragmento por vez
            ydl_opts['fragment_retries'] = 3  # Menos tentativas
            ydl_opts['http_chunk_size'] = None  # Desabilita chunking que causa problemas
            ydl_opts['retries'] = 3
            ydl_opts['http_headers'] = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
            }
        
        if request.audio_only:
            # Áudio apenas - MP3
            ydl_opts['format'] = 'bestaudio/best'
            if self.ffmpeg_location and os.path.exists(self.ffmpeg_location):
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
                ydl_opts['ffmpeg_location'] = os.path.dirname(self.ffmpeg_location)
        else:
            # Vídeo - Detecta se é formato curto ou plataforma sem seleção de qualidade
            is_short_format = (
                platform == 'Instagram' or 
                platform == 'TikTok' or 
                platform == 'Twitter' or
                platform == 'Facebook' or
                '/shorts/' in request.url.lower()
            )
            
            # Reddit precisa de tratamento especial
            if platform == 'Reddit':
                # Reddit tem estrutura de vídeo/áudio separados, precisa merge
                # Precisa de FFmpeg instalado para fazer o merge
                if self.ffmpeg_location and os.path.exists(self.ffmpeg_location):
                    ydl_opts['format'] = 'bestvideo+bestaudio/best'
                    ydl_opts['merge_output_format'] = 'mp4'
                    ydl_opts['ffmpeg_location'] = os.path.dirname(self.ffmpeg_location)
                    print(f"Detectado Reddit - usando formato com merge de vídeo+áudio (FFmpeg disponível)")
                else:
                    # Sem FFmpeg, tenta pegar stream único
                    ydl_opts['format'] = 'best'
                    print(f"Detectado Reddit - usando melhor stream único (FFmpeg não disponível)")
            elif is_short_format:
                # Para vídeos curtos, Twitter e Facebook: apenas o melhor disponível
                ydl_opts['format'] = 'best'
                print(f"Detectado formato curto/social ({platform}) - usando melhor qualidade disponível")
            elif request.quality:
                # Para vídeos longos do YouTube com seleção de qualidade
                heights = {'1080p': 1080, '720p': 720, '480p': 480, '360p': 360}
                h = heights.get(request.quality, 720)
                # Prioriza formatos progressivos (stream único, mais rápido)
                # Formato mais flexível para evitar erros de "formato não disponível"
                ydl_opts['format'] = f'best[height<={h}]/bestvideo[height<={h}]+bestaudio/best'
            else:
                # Padrão: melhor disponível
                ydl_opts['format'] = 'best'
        
        print(f"Formato yt-dlp: {ydl_opts['format']}\n")
        
        try:
            if request.client_id and self.ws_manager:
                self.send_progress_sync(
                    request.client_id, 'starting', 0, 'Iniciando download...'
                )
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print("→ Baixando...")
                info = ydl.extract_info(request.url, download=True)
                
                if not info:
                    raise Exception("Não foi possível baixar o vídeo")
                
                print("✓ Download concluído!")
                
                # Usa o caminho capturado pelo hook ou busca o arquivo
                if downloaded_file_path and os.path.exists(downloaded_file_path):
                    filepath = Path(downloaded_file_path)
                    print(f"✓ Arquivo baixado: {filepath.name}")
                else:
                    # Fallback: busca o arquivo mais recente na pasta temp
                    print("⚠ Caminho não capturado, buscando arquivo mais recente...")
                    files = list(self.temp_path.glob(f"MediaVid{platform}{random_code}.*"))
                    if not files:
                        # Busca qualquer arquivo recente como último recurso
                        files = list(self.temp_path.glob("*.*"))
                    
                    if not files:
                        raise Exception("Nenhum arquivo encontrado após download")
                    
                    # Pega o arquivo mais recente
                    filepath = max(files, key=lambda f: f.stat().st_mtime)
                    print(f"✓ Arquivo encontrado: {filepath.name}")
            
            if request.client_id and self.ws_manager:
                self.send_progress_sync(
                    request.client_id, 'complete', 100, 'Pronto para download!'
                )
            
            print(f"✓ Retornando arquivo: {filepath.name}")
            
            return {
                'success': True,
                'filename': filepath.name,
                'filepath': str(filepath),
                'title': info.get('title'),
                'filesize': os.path.getsize(filepath) if filepath.exists() else None
            }
                
        except Exception as e:
            print(f"\n✗ ERRO: {str(e)}\n")
            if request.client_id and self.ws_manager:
                self.send_progress_sync(
                    request.client_id, 'error', 0, f'Erro: {str(e)}'
                )
            raise Exception(f"Erro ao baixar vídeo: {str(e)}")
    
    def cleanup_file(self, filepath: str):
        """Remove arquivo temporário"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            print(f"Erro ao limpar arquivo {filepath}: {e}")


# Instância global do downloader
downloader = VideoDownloader()
