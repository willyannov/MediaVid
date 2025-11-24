"""
Fallback alternativo para YouTube usando scraping direto
Similar ao y2mate, ytdown, etc
"""
import re
import json
import requests
from typing import Optional, Dict, Any


class YouTubeFallback:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        })
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extrai o ID do vídeo da URL"""
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
            r'(?:embed\/)([0-9A-Za-z_-]{11})',
            r'(?:watch\?v=)([0-9A-Za-z_-]{11})',
            r'^([0-9A-Za-z_-]{11})$',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def get_video_info(self, url: str) -> Optional[Dict[str, Any]]:
        """Obtém informações do vídeo usando scraping direto"""
        try:
            video_id = self.extract_video_id(url)
            if not video_id:
                print("❌ ID do vídeo não encontrado na URL")
                return None
            
            print(f"🔍 Tentando scraping direto do YouTube para: {video_id}")
            
            # Tenta buscar a página do vídeo
            watch_url = f'https://www.youtube.com/watch?v={video_id}'
            response = self.session.get(watch_url, timeout=15)
            
            if response.status_code != 200:
                print(f"❌ Erro ao acessar página: {response.status_code}")
                return None
            
            html = response.text
            
            # Extrai dados do player usando regex
            # Procura por ytInitialPlayerResponse que contém todas as infos
            player_response_match = re.search(
                r'var ytInitialPlayerResponse\s*=\s*({.+?});',
                html
            )
            
            if not player_response_match:
                print("❌ Não foi possível extrair ytInitialPlayerResponse")
                return None
            
            player_data = json.loads(player_response_match.group(1))
            
            # Extrai informações do vídeo
            video_details = player_data.get('videoDetails', {})
            
            if not video_details:
                print("❌ videoDetails não encontrado")
                return None
            
            # Extrai streaming data (formatos de vídeo)
            streaming_data = player_data.get('streamingData', {})
            formats = streaming_data.get('formats', []) + streaming_data.get('adaptiveFormats', [])
            
            # Filtra apenas formatos válidos com URL direta (sem signatureCipher)
            valid_formats = []
            for fmt in formats:
                # Só aceita formatos com URL direta (sem assinatura criptografada)
                if fmt.get('url') and not fmt.get('signatureCipher'):
                    format_info = {
                        'format_id': str(fmt.get('itag', '')),
                        'url': fmt.get('url'),
                        'ext': fmt.get('mimeType', '').split('/')[1].split(';')[0] if fmt.get('mimeType') else 'mp4',
                        'quality': fmt.get('qualityLabel', fmt.get('quality', '')),
                        'filesize': int(fmt.get('contentLength', 0)) if fmt.get('contentLength') else None,
                        'fps': fmt.get('fps'),
                        'width': fmt.get('width'),
                        'height': fmt.get('height'),
                        'vcodec': fmt.get('mimeType', '').split(';')[0].split('/')[-1] if fmt.get('mimeType') else None,
                        'acodec': 'aac' if 'audio' in fmt.get('mimeType', '').lower() else None,
                    }
                    valid_formats.append(format_info)
            
            result = {
                'url': watch_url,
                'title': video_details.get('title', 'Unknown'),
                'description': video_details.get('shortDescription'),
                'thumbnail': video_details.get('thumbnail', {}).get('thumbnails', [{}])[-1].get('url'),
                'duration': int(video_details.get('lengthSeconds', 0)),
                'uploader': video_details.get('author', 'Unknown'),
                'view_count': int(video_details.get('viewCount', 0)),
                'formats': valid_formats,
            }
            
            print(f"✅ Scraping bem sucedido! {len(valid_formats)} formatos encontrados")
            return result
            
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao decodificar JSON: {e}")
            return None
        except Exception as e:
            print(f"❌ Erro no scraping do YouTube: {e}")
            return None
