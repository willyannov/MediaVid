"""
Fallback usando pytubefix para download de vídeos do YouTube.
Usado quando yt-dlp falha devido a bloqueios de bot.
"""

from pytubefix import YouTube
from typing import Optional, Dict, Any


class YouTubeApiFallback:
    """Usa pytubefix como fallback para YouTube"""
    
    def get_video_info(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Extrai informações do vídeo do YouTube usando pytubefix.
        Pytubefix é uma versão mantida e atualizada do pytube.
        """
        try:
            print("🔄 Tentando pytubefix para YouTube...")
            
            yt = YouTube(url)
            
            # Extrai streams de vídeo (progressivo = vídeo+áudio juntos)
            streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
            
            formats = []
            for stream in streams:
                formats.append({
                    'format_id': str(stream.itag),
                    'url': stream.url,
                    'ext': 'mp4',
                    'quality': stream.resolution or 'unknown',
                    'resolution': stream.resolution,
                    'filesize': stream.filesize,
                    'fps': int(stream.fps) if stream.fps else None,
                    'vcodec': stream.video_codec,
                    'acodec': stream.audio_codec,
                })
            
            result = {
                'url': url,
                'title': yt.title,
                'description': yt.description,
                'thumbnail': yt.thumbnail_url,
                'duration': yt.length,
                'uploader': yt.author,
                'view_count': yt.views,
                'formats': formats,
                'source': 'pytubefix',
            }
            
            print(f"✅ Pytubefix: {len(formats)} formatos encontrados!")
            return result
            
        except Exception as e:
            print(f"❌ Erro pytubefix: {e}")
            return None
