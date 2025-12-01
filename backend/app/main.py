from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MediaVid API",
    description="API para download de vídeos de redes sociais",
    version="1.0.0"
)

# CORS Configuration - Permissivo para produção
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition", "Content-Length", "Content-Type"],
    max_age=3600,  # Cache preflight por 1 hora
)


@app.on_event("startup")
async def startup_event():
    logger.info("🚀 MediaVid API iniciando...")
    logger.info(f"✅ Ambiente: {settings.DEBUG and 'development' or 'production'}")
    logger.info(f"✅ CORS Origins: {len(settings.cors_origins)} configurados")


@app.get("/")
async def root():
    return {
        "message": "MediaVid API",
        "version": "1.0.0",
        "status": "online"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Import routes
from app.routes import video, websocket, batch, health
from app.services.downloader import downloader

# Injeta WebSocket manager no downloader
downloader.set_websocket_manager(websocket.manager)

app.include_router(video.router)
app.include_router(websocket.router)
app.include_router(batch.router)
app.include_router(health.router)
