from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.config import settings
import time

router = APIRouter(prefix="/api/health", tags=["health"])

# Armazena timestamp da última requisição
_last_ping = time.time()


@router.get("/")
async def health_check():
    """
    Health check simples para manter servidor ativo
    """
    global _last_ping
    _last_ping = time.time()
    return {"status": "ok", "message": "Server is running"}


@router.get("/ping")
async def ping():
    """
    Endpoint para keep-alive automático
    """
    global _last_ping
    current = time.time()
    uptime = current - _last_ping
    _last_ping = current
    
    return {
        "status": "alive",
        "uptime_seconds": round(uptime, 2),
        "timestamp": current
    }


@router.get("/cors")
async def check_cors():
    """
    Endpoint para verificar configuração CORS
    """
    return JSONResponse(
        content={
            "status": "ok",
            "allowed_origins": settings.cors_origins,
            "message": "CORS está configurado corretamente"
        },
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "*"
        }
    )
