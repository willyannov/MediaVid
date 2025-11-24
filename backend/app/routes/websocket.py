from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json

router = APIRouter()

# Gerenciador de conexões WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        print(f"✓ Cliente WebSocket conectado: {client_id}")
    
    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            print(f"✗ Cliente WebSocket desconectado: {client_id}")
    
    async def send_progress(self, client_id: str, data: dict):
        """Envia atualização de progresso para um cliente específico"""
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_json(data)
            except Exception as e:
                print(f"Erro ao enviar progresso para {client_id}: {e}")
                self.disconnect(client_id)

manager = ConnectionManager()


@router.websocket("/ws/progress/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            # Mantém conexão aberta
            data = await websocket.receive_text()
            # Pode responder com pong se receber ping
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(client_id)
    except Exception as e:
        print(f"Erro no WebSocket {client_id}: {e}")
        manager.disconnect(client_id)
