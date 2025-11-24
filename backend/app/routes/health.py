from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.config import settings

router = APIRouter(prefix="/api/health", tags=["health"])


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
