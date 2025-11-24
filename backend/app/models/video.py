from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from enum import Enum


class FormatType(str, Enum):
    VIDEO = "video"
    AUDIO = "audio"


class VideoFormat(BaseModel):
    format_id: str
    ext: str
    quality: Optional[str] = None
    resolution: Optional[str] = None
    filesize: Optional[int] = None
    format_note: Optional[str] = None
    fps: Optional[float] = None  # Mudado de int para float
    vcodec: Optional[str] = None
    acodec: Optional[str] = None


class VideoInfo(BaseModel):
    url: str
    title: str
    description: Optional[str] = None
    thumbnail: Optional[str] = None
    duration: Optional[float] = None  # Mudado de int para float (aceita decimais)
    uploader: Optional[str] = None
    uploader_url: Optional[str] = None
    view_count: Optional[int] = None
    formats: List[VideoFormat] = []
    platform: Optional[str] = None


class DownloadRequest(BaseModel):
    url: str = Field(..., description="URL do vídeo")
    format_id: Optional[str] = Field(None, description="ID do formato específico")
    audio_only: bool = Field(False, description="Baixar apenas áudio")
    quality: Optional[str] = Field(None, description="Qualidade desejada (e.g., '1080p', '720p')")
    output_format: Optional[str] = Field(None, description="Formato de saída (mp4, webm, mp3, etc)")
    client_id: Optional[str] = Field(None, description="ID do cliente para WebSocket")


class DownloadResponse(BaseModel):
    success: bool
    message: str
    filename: Optional[str] = None
    download_url: Optional[str] = None
