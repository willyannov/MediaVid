from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, StreamingResponse
from typing import List
from app.models.video import DownloadRequest
from app.services.downloader import downloader
from app.services.queue_manager import queue_manager, DownloadStatus
from app.utils.validators import validate_url
import asyncio
import os

router = APIRouter(prefix="/api/batch", tags=["batch"])


@router.post("/add")
async def add_to_batch(items: List[DownloadRequest]):
    """
    Adiciona múltiplos vídeos à fila de download em lote
    """
    if not items:
        raise HTTPException(status_code=400, detail="Lista de itens vazia")
    
    # Valida todas as URLs
    for item in items:
        if not validate_url(item.url):
            raise HTTPException(status_code=400, detail=f"URL inválida: {item.url}")
    
    try:
        # Adiciona itens à fila
        item_ids = []
        for item in items:
            item_id = queue_manager.add_to_queue(
                url=item.url,
                quality=item.quality,
                output_format=item.output_format or ('mp3' if item.audio_only else 'mp4'),
                audio_only=item.audio_only
            )
            item_ids.append(item_id)
        
        return {
            "success": True,
            "message": f"{len(item_ids)} itens adicionados à fila",
            "item_ids": item_ids,
            "queue_status": queue_manager.get_queue_status()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/queue")
async def get_queue():
    """
    Retorna o estado atual da fila
    """
    items = queue_manager.get_all_items()
    return {
        "items": [
            {
                "id": item.id,
                "url": item.url,
                "quality": item.quality,
                "output_format": item.output_format,
                "audio_only": item.audio_only,
                "status": item.status,
                "progress": item.progress,
                "message": item.message,
                "filepath": item.filepath,
                "error": item.error,
                "downloaded": item.downloaded,
                "created_at": item.created_at.isoformat() if item.created_at else None,
                "started_at": item.started_at.isoformat() if item.started_at else None,
                "completed_at": item.completed_at.isoformat() if item.completed_at else None
            }
            for item in items
        ],
        "status": queue_manager.get_queue_status()
    }


@router.post("/start")
async def start_batch_download(background_tasks: BackgroundTasks):
    """
    Inicia o processamento da fila de downloads
    """
    items = queue_manager.get_all_items()
    pending_items = [item for item in items if item.status == DownloadStatus.PENDING]
    
    if not pending_items:
        raise HTTPException(status_code=400, detail="Não há itens pendentes na fila")
    
    # Inicia processamento em background
    background_tasks.add_task(process_queue)
    
    return {
        "success": True,
        "message": f"Processando {len(pending_items)} itens",
        "queue_status": queue_manager.get_queue_status()
    }


async def process_queue():
    """
    Processa a fila de downloads (até max_concurrent simultâneos)
    """
    items = queue_manager.get_all_items()
    pending_items = [item for item in items if item.status == DownloadStatus.PENDING]
    
    async def download_item(item):
        """Download de um item individual"""
        try:
            queue_manager.update_status(item.id, DownloadStatus.DOWNLOADING, 0, "Iniciando download...")
            
            # Cria request para o downloader
            request = DownloadRequest(
                url=item.url,
                format_id=None,  # Não usamos format_id específico
                quality=item.quality,
                output_format=item.output_format,
                audio_only=item.audio_only,
                client_id=item.id  # Usa o ID do item como client_id para WebSocket
            )
            
            # Executa download
            result = downloader.download_video(request)
            
            if result['success']:
                queue_manager.set_filepath(item.id, result['filepath'])
                queue_manager.update_status(item.id, DownloadStatus.COMPLETED, 100, "Download concluído!")
            else:
                queue_manager.set_error(item.id, "Falha no download")
        
        except Exception as e:
            queue_manager.set_error(item.id, str(e))
    
    # Processa itens com semáforo (controle de concorrência)
    tasks = []
    for item in pending_items:
        if item.status == DownloadStatus.PENDING:  # Verifica novamente (pode ter sido cancelado)
            async with queue_manager.semaphore:
                task = asyncio.create_task(download_item(item))
                queue_manager.active_downloads[item.id] = task
                tasks.append(task)
    
    # Aguarda todos completarem
    await asyncio.gather(*tasks, return_exceptions=True)
    
    # Limpa downloads ativos
    queue_manager.active_downloads.clear()


@router.post("/item/{item_id}/cancel")
async def cancel_item(item_id: str):
    """
    Cancela um item da fila
    """
    item = queue_manager.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    
    queue_manager.cancel_item(item_id)
    
    return {
        "success": True,
        "message": "Item cancelado",
        "item_id": item_id
    }


@router.post("/item/{item_id}/pause")
async def pause_item(item_id: str):
    """
    Pausa um item pendente
    """
    item = queue_manager.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    
    queue_manager.pause_item(item_id)
    
    return {
        "success": True,
        "message": "Item pausado",
        "item_id": item_id
    }


@router.post("/item/{item_id}/resume")
async def resume_item(item_id: str):
    """
    Resume um item pausado
    """
    item = queue_manager.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    
    queue_manager.resume_item(item_id)
    
    return {
        "success": True,
        "message": "Item retomado",
        "item_id": item_id
    }


@router.delete("/clear/completed")
async def clear_completed():
    """
    Remove itens completados da fila
    """
    queue_manager.clear_completed()
    return {
        "success": True,
        "message": "Itens completados removidos"
    }


@router.delete("/clear/all")
async def clear_all():
    """
    Limpa toda a fila
    """
    queue_manager.clear_all()
    return {
        "success": True,
        "message": "Fila limpa"
    }


@router.get("/item/{item_id}/download")
async def download_batch_item(item_id: str, background_tasks: BackgroundTasks):
    """
    Faz download de um item específico que já foi baixado
    """
    item = queue_manager.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    
    if item.status != DownloadStatus.COMPLETED or not item.filepath:
        raise HTTPException(status_code=400, detail="Item ainda não foi baixado ou falhou")
    
    if not os.path.exists(item.filepath):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado no servidor")
    
    filename = os.path.basename(item.filepath)
    
    # Agenda limpeza do arquivo após enviar
    background_tasks.add_task(downloader.cleanup_file, item.filepath)
    
    # Marca que o arquivo foi baixado pelo usuário
    queue_manager.mark_as_downloaded(item_id)
    
    return FileResponse(
        path=item.filepath,
        media_type='application/octet-stream',
        filename=filename
    )
