"""
Fallback usando APIs públicas para download de vídeos do YouTube.
Usado quando yt-dlp falha devido a bloqueios de bot.
"""

import requests
from typing import Optional, Dict, Any
import json


class YouTubeApiFallback:
    """Usa APIs públicas como fallback para YouTube"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extrai o ID do vídeo da URL do YouTube"""
        import re
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
            r'youtube\.com\/shorts\/([^&\n?#]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def get_video_info_cobalt(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Tenta usar Cobalt API (co.wuk.sh) - API gratuita e open-source
        Documentação: https://github.com/wukko/cobalt
        """
        try:
            video_id = self.extract_video_id(url)
            if not video_id:
                return None
            
            print("🔄 Tentando Cobalt API para YouTube...")
            
            # Cobalt API endpoint
            api_url = "https://co.wuk.sh/api/json"
            
            payload = {
                "url": url,
                "vCodec": "h264",
                "vQuality": "720",
                "aFormat": "mp3",
                "isAudioOnly": False,
                "isNoTTWatermark": True,
            }
            
            response = self.session.post(
                api_url,
                json=payload,
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'redirect' or data.get('status') == 'stream':
                    download_url = data.get('url')
                    
                    if download_url:
                        print("✅ Cobalt API: URL de download obtida!")
                        return {
                            'url': url,
                            'download_url': download_url,
                            'title': f'YouTube Video {video_id}',
                            'source': 'cobalt',
                            'formats': [{
                                'format_id': '720p',
                                'url': download_url,
                                'ext': 'mp4',
                                'quality': '720p',
                            }]
                        }
            
            print(f"⚠️ Cobalt API falhou: {response.status_code}")
            return None
            
        except Exception as e:
            print(f"❌ Erro Cobalt API: {e}")
            return None
    
    def get_video_info_y2mate(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Tenta usar Y2Mate API não-oficial
        NOTA: APIs não-oficiais podem parar de funcionar
        """
        try:
            video_id = self.extract_video_id(url)
            if not video_id:
                return None
            
            print("🔄 Tentando Y2Mate API para YouTube...")
            
            # Y2Mate tem vários endpoints, tentamos o mais estável
            api_url = f"https://www.y2mate.com/mates/analyzeV2/ajax"
            
            payload = {
                'k_query': url,
                'k_page': 'home',
                'hl': 'en',
                'q_auto': '0'
            }
            
            response = self.session.post(api_url, data=payload, timeout=20)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'ok':
                    links = data.get('links', {})
                    mp4_links = links.get('mp4', {})
                    
                    if mp4_links:
                        # Pega o melhor formato disponível
                        best_quality = None
                        for quality_key in ['720', '480', '360', '144']:
                            if quality_key in mp4_links:
                                best_quality = mp4_links[quality_key]
                                break
                        
                        if best_quality:
                            print(f"✅ Y2Mate API: Formato {quality_key}p encontrado!")
                            return {
                                'url': url,
                                'title': data.get('title', f'YouTube Video {video_id}'),
                                'duration': data.get('t', 0),
                                'source': 'y2mate',
                                'formats': [{
                                    'format_id': quality_key + 'p',
                                    'quality': quality_key + 'p',
                                    'ext': 'mp4',
                                    'k': best_quality.get('k'),  # Token necessário para download
                                }]
                            }
            
            print(f"⚠️ Y2Mate API falhou: {response.status_code}")
            return None
            
        except Exception as e:
            print(f"❌ Erro Y2Mate API: {e}")
            return None
    
    def get_video_info_invidious(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Tenta usar Invidious API - Frontend alternativo do YouTube
        Instâncias públicas: https://docs.invidious.io/instances/
        """
        try:
            video_id = self.extract_video_id(url)
            if not video_id:
                return None
            
            print("🔄 Tentando Invidious API para YouTube...")
            
            # Lista de instâncias públicas do Invidious (pode variar)
            invidious_instances = [
                "https://invidious.privacydev.net",
                "https://invidious.fdn.fr",
                "https://inv.nadeko.net",
            ]
            
            for instance in invidious_instances:
                try:
                    api_url = f"{instance}/api/v1/videos/{video_id}"
                    response = self.session.get(api_url, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        formats = []
                        for fmt in data.get('formatStreams', []):
                            if fmt.get('type', '').startswith('video/mp4'):
                                formats.append({
                                    'format_id': fmt.get('qualityLabel', fmt.get('quality', '')),
                                    'url': fmt.get('url'),
                                    'ext': 'mp4',
                                    'quality': fmt.get('qualityLabel', fmt.get('quality', '')),
                                    'filesize': fmt.get('size'),
                                })
                        
                        if formats:
                            print(f"✅ Invidious API ({instance}): {len(formats)} formatos encontrados!")
                            return {
                                'url': url,
                                'title': data.get('title', f'YouTube Video {video_id}'),
                                'description': data.get('description'),
                                'thumbnail': data.get('videoThumbnails', [{}])[0].get('url'),
                                'duration': data.get('lengthSeconds', 0),
                                'uploader': data.get('author', 'Unknown'),
                                'view_count': data.get('viewCount', 0),
                                'source': 'invidious',
                                'formats': formats,
                            }
                
                except Exception as e:
                    print(f"⚠️ Instância {instance} falhou: {e}")
                    continue
            
            print("⚠️ Todas instâncias Invidious falharam")
            return None
            
        except Exception as e:
            print(f"❌ Erro Invidious API: {e}")
            return None
    
    def get_video_info(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Tenta múltiplas APIs em ordem de prioridade.
        Retorna no primeiro sucesso.
        """
        print("🎬 Iniciando fallback de APIs para YouTube...")
        
        # Ordem de tentativas (mais confiável primeiro)
        apis = [
            ('Invidious', self.get_video_info_invidious),
            ('Cobalt', self.get_video_info_cobalt),
            ('Y2Mate', self.get_video_info_y2mate),
        ]
        
        for api_name, api_func in apis:
            try:
                result = api_func(url)
                if result:
                    print(f"✅ Sucesso com {api_name} API!")
                    return result
            except Exception as e:
                print(f"❌ {api_name} API falhou: {e}")
                continue
        
        print("❌ Todas as APIs de fallback falharam")
        return None
