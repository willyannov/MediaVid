from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, StreamingResponse
from app.models.video import VideoInfo, DownloadRequest, DownloadResponse
from app.services.downloader import downloader
from app.utils.validators import validate_url, detect_platform
import os
import requests

router = APIRouter(prefix="/api/video", tags=["video"])


@router.post("/info", response_model=VideoInfo)
async def get_video_info(request: dict):
    """
    Obtém informações sobre o vídeo sem baixá-lo
    """
    url = request.get("url")
    
    if not url:
        raise HTTPException(status_code=400, detail="URL é obrigatória")
    
    if not validate_url(url):
        raise HTTPException(status_code=400, detail="URL inválida")
    
    # Valida plataforma suportada
    platform = detect_platform(url)
    if platform == 'Unknown':
        raise HTTPException(
            status_code=400, 
            detail="Plataforma não suportada. Atualmente suportamos: Instagram, TikTok, Twitter/X, Facebook e Reddit."
        )
    
    try:
        video_info = downloader.get_video_info(url)
        return video_info
    except Exception as e:
        error_msg = str(e)
        # Se demorar muito ou falhar, retorna mensagem amigável
        if 'timeout' in error_msg.lower() or 'timed out' in error_msg.lower():
            raise HTTPException(
                status_code=408, 
                detail="Tempo limite excedido. Tente novamente ou verifique se o vídeo é público."
            )
        raise HTTPException(status_code=500, detail=error_msg)


@router.post("/download")
async def download_video(request: DownloadRequest, background_tasks: BackgroundTasks):
    """
    Faz o download do vídeo e retorna o arquivo
    """
    if not validate_url(request.url):
        raise HTTPException(status_code=400, detail="URL inválida")
    
    try:
        # Baixa o vídeo (agora com suporte a client_id para WebSocket)
        result = downloader.download_video(request)
        
        if not result['success']:
            raise HTTPException(status_code=500, detail="Erro ao baixar vídeo")
        
        filepath = result['filepath']
        
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="Arquivo não encontrado")
        
        # Agenda limpeza do arquivo após enviar
        background_tasks.add_task(downloader.cleanup_file, filepath)
        
        # Retorna o arquivo para download com header correto
        headers = {
            'Content-Disposition': f'attachment; filename="{result["filename"]}"'
        }
        
        return FileResponse(
            path=filepath,
            filename=result['filename'],
            media_type='application/octet-stream',
            headers=headers
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/formats")
async def get_available_formats():
    """
    Retorna os formatos disponíveis
    """
    return {
        "quality_options": [
            {"value": "1080p", "label": "Full HD 1080p"},
            {"value": "720p", "label": "HD 720p"},
            {"value": "480p", "label": "SD 480p"},
            {"value": "360p", "label": "Low 360p"}
        ]
    }


@router.get("/proxy-thumbnail")
async def proxy_thumbnail(url: str):
    """
    Proxy para thumbnails do Instagram (evita bloqueio CORS)
    """
    if not url:
        raise HTTPException(status_code=400, detail="URL da thumbnail é obrigatória")
    
    try:
        # Faz requisição com headers de navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Referer': 'https://www.instagram.com/',
            'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Retorna a imagem com headers CORS apropriados
        return StreamingResponse(
            iter([response.content]),
            media_type=response.headers.get('content-type', 'image/jpeg'),
            headers={
                'Access-Control-Allow-Origin': '*',
                'Cache-Control': 'public, max-age=3600'
            }
        )
        
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar thumbnail: {str(e)}")
