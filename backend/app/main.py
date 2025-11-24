from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

app = FastAPI(
    title="MediaVid API",
    description="API para download de vídeos de redes sociais",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],  # Expor header customizado
)


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
from app.routes import video, websocket, batch
from app.services.downloader import downloader

# Injeta WebSocket manager no downloader
downloader.set_websocket_manager(websocket.manager)

app.include_router(video.router)
app.include_router(websocket.router)
app.include_router(batch.router)
