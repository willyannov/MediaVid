import re
from typing import Optional


def validate_url(url: str) -> bool:
    """Valida se a URL é válida"""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None


def detect_platform(url: str) -> Optional[str]:
    """Detecta a plataforma baseada na URL"""
    url_lower = url.lower()
    
    # Detecta plataformas com padrões específicos
    if 'youtube.com' in url_lower or 'youtu.be' in url_lower:
        return 'YouTube'
    elif 'instagram.com' in url_lower:
        return 'Instagram'
    elif 'tiktok.com' in url_lower:
        return 'TikTok'
    elif 'twitter.com' in url_lower or 'x.com' in url_lower:
        return 'Twitter'
    elif 'facebook.com' in url_lower or 'fb.watch' in url_lower:
        return 'Facebook'
    elif 'reddit.com' in url_lower:
        return 'Reddit'
    
    return 'Unknown'


def format_filesize(size_bytes: Optional[int]) -> str:
    """Formata o tamanho do arquivo em formato legível"""
    if not size_bytes:
        return "Unknown"
    
    size = float(size_bytes)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"


def sanitize_filename(filename: str) -> str:
    """Remove caracteres inválidos do nome do arquivo"""
    # Remove caracteres inválidos para Windows/Linux
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename.strip()
