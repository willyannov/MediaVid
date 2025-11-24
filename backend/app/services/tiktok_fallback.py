"""
Fallback para download de TikTok usando APIs alternativas
quando yt-dlp falha por restrição de login
"""
import requests
import re
import json
from typing import Optional, Dict, Any


class TikTokFallback:
    """Serviço alternativo para baixar vídeos do TikTok"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.tiktok.com/'
        })
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extrai o ID do vídeo da URL"""
        patterns = [
            r'/video/(\d+)',
            r'tiktok\.com/@[\w.-]+/video/(\d+)',
            r'vm\.tiktok\.com/(\w+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def get_video_info_api(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Tenta obter informações usando API alternativa (estilo ssstik.io)"""
        try:
            # API 1: TikWM (funciona sem login)
            api_url = f"https://www.tikwm.com/api/?url=https://www.tiktok.com/@user/video/{video_id}"
            
            response = self.session.get(api_url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                
                if data.get('code') == 0 and data.get('data'):
                    video_data = data['data']
                    return {
                        'url': f"https://www.tiktok.com/@{video_data.get('author', {}).get('unique_id', 'user')}/video/{video_id}",
                        'title': video_data.get('title', 'TikTok Video'),
                        'description': video_data.get('title'),
                        'thumbnail': video_data.get('cover', ''),
                        'duration': video_data.get('duration', 0),
                        'uploader': video_data.get('author', {}).get('unique_id', 'Unknown'),
                        'view_count': video_data.get('play_count', 0),
                        'download_url': video_data.get('play', ''),  # URL de download direto
                        'platform': 'TikTok'
                    }
        except Exception as e:
            print(f"Erro API TikWM: {e}")
        
        # Fallback para API 2
        try:
            # API 2: SnapTik (backup)
            api_url = "https://snaptik.app/abc2.php"
            payload = {
                'url': f"https://www.tiktok.com/@user/video/{video_id}",
                'lang': 'en'
            }
            
            response = self.session.post(api_url, data=payload, timeout=15)
            if response.status_code == 200:
                # Parse HTML para extrair links de download
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Procura por links de download
                download_link = soup.find('a', {'class': 'download-file'})
                if download_link and download_link.get('href'):
                    return {
                        'url': f"https://www.tiktok.com/@user/video/{video_id}",
                        'title': 'TikTok Video',
                        'description': None,
                        'thumbnail': None,
                        'duration': 0,
                        'uploader': 'Unknown',
                        'view_count': None,
                        'download_url': download_link['href'],
                        'platform': 'TikTok'
                    }
        except Exception as e:
            print(f"Erro API SnapTik: {e}")
        
        return None
    
    def download_video(self, url: str, output_path: str) -> bool:
        """Baixa o vídeo diretamente da URL de download"""
        try:
            response = self.session.get(url, stream=True, timeout=30)
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                return True
        except Exception as e:
            print(f"Erro ao baixar vídeo do TikTok: {e}")
        return False
    
    def get_video_info(self, url: str) -> Optional[Dict[str, Any]]:
        """Método principal para obter informações do vídeo"""
        video_id = self.extract_video_id(url)
        if not video_id:
            return None
        
        return self.get_video_info_api(video_id)
