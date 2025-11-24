from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000,https://mediavid-frontend.onrender.com"
    
    # Download Settings
    MAX_CONCURRENT_DOWNLOADS: int = 3
    TEMP_DOWNLOAD_PATH: str = "./temp_downloads"
    MAX_FILE_SIZE_MB: int = 500
    
    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE: int = 30
    
    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
