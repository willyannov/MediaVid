import asyncio
from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import uuid


class DownloadStatus(str, Enum):
    PENDING = "pending"
    DOWNLOADING = "downloading"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


@dataclass
class QueueItem:
    id: str
    url: str
    quality: Optional[str]
    output_format: str
    audio_only: bool
    status: DownloadStatus = DownloadStatus.PENDING
    progress: int = 0
    message: str = ""
    filepath: Optional[str] = None
    error: Optional[str] = None
    downloaded: bool = False  # Flag para indicar se usuário já baixou
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class DownloadQueueManager:
    def __init__(self, max_concurrent: int = 3):
        self.max_concurrent = max_concurrent
        self.queue: Dict[str, QueueItem] = {}
        self.active_downloads: Dict[str, asyncio.Task] = {}
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    def add_to_queue(self, url: str, quality: Optional[str], output_format: str, audio_only: bool) -> str:
        """Adiciona item à fila e retorna o ID"""
        item_id = str(uuid.uuid4())
        item = QueueItem(
            id=item_id,
            url=url,
            quality=quality,
            output_format=output_format,
            audio_only=audio_only
        )
        self.queue[item_id] = item
        return item_id
    
    def add_multiple(self, items: List[Dict]) -> List[str]:
        """Adiciona múltiplos itens à fila"""
        ids = []
        for item in items:
            item_id = self.add_to_queue(
                url=item['url'],
                quality=item.get('quality'),
                output_format=item.get('output_format', 'mp4'),
                audio_only=item.get('audio_only', False)
            )
            ids.append(item_id)
        return ids
    
    def get_item(self, item_id: str) -> Optional[QueueItem]:
        """Retorna item da fila"""
        return self.queue.get(item_id)
    
    def get_all_items(self) -> List[QueueItem]:
        """Retorna todos os itens da fila"""
        return list(self.queue.values())
    
    def get_queue_status(self) -> Dict:
        """Retorna status geral da fila"""
        items = self.get_all_items()
        return {
            'total': len(items),
            'pending': len([i for i in items if i.status == DownloadStatus.PENDING]),
            'downloading': len([i for i in items if i.status == DownloadStatus.DOWNLOADING]),
            'completed': len([i for i in items if i.status == DownloadStatus.COMPLETED]),
            'failed': len([i for i in items if i.status == DownloadStatus.FAILED]),
            'cancelled': len([i for i in items if i.status == DownloadStatus.CANCELLED]),
            'paused': len([i for i in items if i.status == DownloadStatus.PAUSED]),
        }
    
    def update_status(self, item_id: str, status: DownloadStatus, progress: int = 0, message: str = ""):
        """Atualiza status de um item"""
        if item_id in self.queue:
            self.queue[item_id].status = status
            self.queue[item_id].progress = progress
            self.queue[item_id].message = message
            
            if status == DownloadStatus.DOWNLOADING and not self.queue[item_id].started_at:
                self.queue[item_id].started_at = datetime.now()
            elif status in [DownloadStatus.COMPLETED, DownloadStatus.FAILED, DownloadStatus.CANCELLED]:
                self.queue[item_id].completed_at = datetime.now()
    
    def set_error(self, item_id: str, error: str):
        """Define erro para um item"""
        if item_id in self.queue:
            self.queue[item_id].status = DownloadStatus.FAILED
            self.queue[item_id].error = error
            self.queue[item_id].completed_at = datetime.now()
    
    def set_filepath(self, item_id: str, filepath: str):
        """Define caminho do arquivo baixado"""
        if item_id in self.queue:
            self.queue[item_id].filepath = filepath
    
    def cancel_item(self, item_id: str):
        """Cancela um item da fila"""
        if item_id in self.queue:
            self.queue[item_id].status = DownloadStatus.CANCELLED
            self.queue[item_id].completed_at = datetime.now()
            
            # Cancela task ativa se existir
            if item_id in self.active_downloads:
                self.active_downloads[item_id].cancel()
                del self.active_downloads[item_id]
    
    def pause_item(self, item_id: str):
        """Pausa um item (marca como pausado, mas não cancela o download em andamento)"""
        if item_id in self.queue and self.queue[item_id].status == DownloadStatus.PENDING:
            self.queue[item_id].status = DownloadStatus.PAUSED
    
    def resume_item(self, item_id: str):
        """Resume um item pausado"""
        if item_id in self.queue and self.queue[item_id].status == DownloadStatus.PAUSED:
            self.queue[item_id].status = DownloadStatus.PENDING
    
    def clear_completed(self):
        """Remove itens completados da fila"""
        to_remove = [
            item_id for item_id, item in self.queue.items()
            if item.status in [DownloadStatus.COMPLETED, DownloadStatus.FAILED, DownloadStatus.CANCELLED]
        ]
        for item_id in to_remove:
            del self.queue[item_id]
    
    def clear_all(self):
        """Limpa toda a fila"""
        # Cancela downloads ativos
        for task in self.active_downloads.values():
            task.cancel()
        self.active_downloads.clear()
        self.queue.clear()
    
    def mark_as_downloaded(self, item_id: str):
        """Marca item como já baixado pelo usuário"""
        if item_id in self.queue:
            self.queue[item_id].downloaded = True


# Instância global do gerenciador de fila
queue_manager = DownloadQueueManager(max_concurrent=3)
