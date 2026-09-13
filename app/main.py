"""Main FastAPI application."""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

from app.routes import api
from app.core.logging_config import setup_logging, logger
from app.models.database import init_db
from config import settings

# Setup logging
logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup."""
    # Initialize database
    init_db()
    logger.info("Database initialized")
    
    # Create necessary directories
    os.makedirs(settings.AUDIO_DIR, exist_ok=True)
    os.makedirs(settings.RECORDINGS_DIR, exist_ok=True)
    logger.info("Directories created")
    
    yield
    
    logger.info("Application shutdown complete")


app = FastAPI(
    title=settings.APP_NAME,
    description="AI Voice Receptionist Platform - Handle business calls with AI",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware (restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api.router)


@app.get("/", response_class=HTMLResponse)
async def root():
    """Return landing page."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ConvertX Ops - AI Voice Receptionist</title>
        <style>
            body { font-family: system-ui; max-width: 800px; margin: 40px auto; padding: 20px; }
            .card { background: #f5f5f5; padding: 20px; border-radius: 8px; margin: 20px 0; }
            .status { color: green; font-weight: bold; }
            code { background: #eee; padding: 2px 6px; border-radius: 4px; }
        </style>
    </head>
    <body>
        <h1>🎙️ ConvertX Voice Agent</h1>
        <div class="card">
            <h2>✅ System Status: Running</h2>
            <p><strong>Version:</strong> 2.0.0</p>
            <p><strong>API:</strong> <a href="/docs">Swagger Documentation</a></p>
            <p><strong>Health:</strong> <span class="status">Healthy</span></p>
        </div>
        
        <h2>Features</h2>
        <ul>
            <li>📞 <strong>Incoming Calls</strong> - AI answers business phones 24/7</li>
            <li>🗣️ <strong>Voice Conversations</strong> - Natural speech recognition & synthesis</li>
            <li>📅 <strong>Appointment Booking</strong> - Check availability & book slots</li>
            <li>👥 <strong>Lead Capture</strong> - Store caller information automatically</li>
            <li>🔄 <strong>Human Transfer</strong> - Escalate complex calls to staff</li>
            <li>🏢 <strong>Multi-Business</strong> - Configure different businesses independently</li>
        </ul>
        
        <h2>API Endpoints</h2>
        <ul>
            <li><code>POST /api/v1/calls/incoming</code> - Handle incoming calls</li>
            <li><code>GET /api/v1/health</code> - Health check</li>
            <li><code>POST /api/v1/transcribe</code> - Transcribe audio</li>
            <li><code>POST /api/v1/speak</code> - Generate speech</li>
        </ul>
        
        <p style="color: #666;">Powered by Ollama + Whisper + Edge TTS</p>
    </body>
    </html>
    """


@app.get("/uploads/audio/{filename}")
async def serve_audio(filename: str):
    """Serve generated audio files."""
    from fastapi.responses import FileResponse
    file_path = os.path.join(settings.AUDIO_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )