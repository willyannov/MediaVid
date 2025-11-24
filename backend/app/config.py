from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS - Permitir acesso do domínio customizado e redes sociais
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000,https://mediavid-0bvc.onrender.com,https://mediavid.site,https://www.mediavid.site,https://facebook.com,https://www.facebook.com,https://instagram.com,https://www.instagram.com,https://twitter.com,https://x.com,https://tiktok.com,https://www.tiktok.com,https://youtube.com,https://www.youtube.com,https://reddit.com,https://www.reddit.com"
    
    # Download Settings
    MAX_CONCURRENT_DOWNLOADS: int = 3
    TEMP_DOWNLOAD_PATH: str = "./temp_downloads"
    MAX_FILE_SIZE_MB: int = 500
    
    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE: int = 30
    
    # YouTube Cookies (opcional - para produção)
    # Exportar cookies do navegador em modo anônimo seguindo:
    # https://github.com/yt-dlp/yt-dlp/wiki/Extractors#exporting-youtube-cookies
    YOUTUBE_COOKIES: str = ""  # Conteúdo do arquivo cookies.txt
    
    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
