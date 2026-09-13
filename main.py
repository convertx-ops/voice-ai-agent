"""
Voice AI Agent - Main Application
Real-time voice conversations with AI using Ollama + TTS
"""
import os
import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional, Dict, List

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama

from config import settings
from database import init_db, get_db_session
from models import User, Conversation, Message
from agents import get_agent_response
from voice import transcribe_audio, generate_speech

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize DB and start background tasks."""
    await init_db()
    logger.info("Voice AI Agent started")
    yield
    logger.info("Voice AI Agent shutdown")


app = FastAPI(
    title="Voice AI Agent",
    description="AI-powered voice conversations for interview prep, objection handling, and more",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "service": "Voice AI Agent",
        "version": "1.0.0",
        "status": "running",
        "features": [
            "Interview Prep Mode",
            "Objection Handling Mode",
            "Boyfriend/Girlfriend Chat Mode",
            "Custom Persona Support"
        ]
    }


@app.get("/health")
async def health_check():
    try:
        # Check Ollama
        ollama.list()
        ollama_status = "healthy"
    except Exception as e:
        ollama_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "healthy",
        "ollama": ollama_status,
        "model": settings.OLLAMA_MODEL,
        "timestamp": datetime.now().isoformat()
    }


class TranscriptionRequest(BaseModel):
    user_id: str
    mode: str = "interview"
    audio_data: str  # base64 encoded audio


class TranscriptionResponse(BaseModel):
    text: str
    response_text: str
    audio_url: Optional[str] = None
    mode: str


@app.post("/api/v1/transcribe", response_model=TranscriptionResponse)
async def transcribe_and_respond(
    request: TranscriptionRequest,
    background_tasks: BackgroundTasks
):
    """Transcribe voice input and generate AI response with speech."""
    
    # Extract user ID and mode
    user_id = request.user_id
    mode = request.mode
    
    # Validate mode
    valid_modes = ["interview", "objection", "bf_gf", "custom"]
    if mode not in valid_modes:
        raise HTTPException(status_code=400, detail=f"Invalid mode. Choose from: {valid_modes}")
    
    try:
        # Step 1: Transcribe audio
        logger.info(f"Transcribing audio for user {user_id}")
        transcription = await transcribe_audio(request.audio_data)
        
        # Step 2: Get AI response
        logger.info(f"Getting AI response for mode: {mode}")
        ai_response = await get_agent_response(mode, transcription, user_id)
        
        # Step 3: Generate speech (background task)
        audio_url = None
        if settings.ENABLE_TTS:
            async def _generate_audio():
                nonlocal audio_url
                audio_url = await generate_speech(ai_response, user_id, mode)
            background_tasks.add_task(_generate_audio)
        
        # Save conversation to database
        db = next(get_db_session())
        conversation = Conversation(
            user_id=user_id,
            mode=mode,
            timestamp=datetime.now()
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        
        message = Message(
            conversation_id=conversation.id,
            role="user",
            content=transcription
        )
        db.add(message)
        
        message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=ai_response
        )
        db.add(message)
        db.commit()
        
        return TranscriptionResponse(
            text=transcription,
            response_text=ai_response,
            audio_url=audio_url,
            mode=mode
        )
        
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/conversations/{user_id}")
async def get_conversations(user_id: str, limit: int = 10):
    """Get conversation history for a user."""
    db = next(get_db_session())
    conversations = db.query(Conversation).filter(
        Conversation.user_id == user_id
    ).order_by(
        Conversation.timestamp.desc()
    ).limit(limit).all()
    
    result = []
    for conv in conversations:
        messages = db.query(Message).filter(
            Message.conversation_id == conv.id
        ).order_by(Message.timestamp.asc()).all()
        
        result.append({
            "id": conv.id,
            "mode": conv.mode,
            "timestamp": conv.timestamp.isoformat(),
            "messages": [
                {"role": m.role, "content": m.content}
                for m in messages
            ]
        })
    
    return result


@app.get("/api/v1/modes")
async def get_available_modes():
    """List available conversation modes."""
    return {
        "modes": [
            {
                "id": "interview",
                "name": "Interview Prep",
                "description": "Practice job interviews with AI interviewer",
                "premium": False
            },
            {
                "id": "objection",
                "name": "Objection Handling",
                "description": "Practice sales objection handling",
                "premium": False
            },
            {
                "id": "bf_gf",
                "name": "Boyfriend/Girlfriend Chat",
                "description": "Casual conversational practice",
                "premium": True
            },
            {
                "id": "custom",
                "name": "Custom Persona",
                "description": "Create your own AI persona",
                "premium": True
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
