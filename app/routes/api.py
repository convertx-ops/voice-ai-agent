"""FastAPI routes for the Voice Agent."""
import logging
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.logging_config import logger
from app.models.database import get_db
from app.services.telephony import telephony
from app.services.call_session import call_manager
from app.services.voice import voice_service
from app.services.agent import agent
from config import settings

router = APIRouter(prefix="/api/v1", tags=["Voice Agent"])


# ===== Request/Response Models =====

class BusinessCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    timezone: str = "UTC"
    language: str = "en"


class CallWebhook(BaseModel):
    call_sid: str
    from_number: str
    to_number: str
    status: str


class CallResponse(BaseModel):
    success: bool
    session_id: Optional[str] = None
    message: Optional[str] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    services: dict
    uptime: str


class StatsResponse(BaseModel):
    active_calls: int
    max_concurrent: int
    total_sessions: int


# ===== Health & Status =====

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check system health."""
    return HealthResponse(
        status="healthy",
        services={
            "database": "connected",
            "voice_service": "ready",
            "agent": "ready",
            "telephony": telephony.provider or "not_configured"
        },
        uptime="running"
    )


@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get system statistics."""
    stats = call_manager.get_stats()
    return StatsResponse(**stats)


# ===== Business Management =====

@router.post("/businesses", response_model=dict)
async def create_business(
    business: BusinessCreate,
    db: Session = Depends(get_db)
):
    """Create a new business."""
    # TODO: Implement actual business creation
    return {
        "id": 1,
        "name": business.name,
        "slug": business.slug,
        "message": "Business created (demo mode)"
    }


@router.get("/businesses/{slug}", response_model=dict)
async def get_business(slug: str):
    """Get business configuration."""
    # TODO: Query database
    return {
        "slug": slug,
        "name": f"Demo Business: {slug}",
        "timezone": "UTC",
        "config": {
            "business_hours": "Mon-Fri 9AM-5PM",
            "address": "123 Main St, City, State",
            "contact_phone": "+1234567890",
            "transfer_phone": "+1234567890"
        }
    }


# ===== Call Handling =====

@router.post("/calls/incoming", response_model=CallResponse)
async def handle_incoming_call(webhook: CallWebhook):
    """
    Handle incoming call webhook from telephony provider.
    
    This endpoint is called by Twilio/Telnyx when a call comes in.
    """
    logger.info(f"Incoming call webhook: {webhook.call_sid} from {webhook.from_number}")
    
    result = await telephony.handle_incoming_call(
        caller_number=webhook.from_number,
        business_slug="demo",  # Would parse from phone number
        call_sid=webhook.call_sid
    )
    
    return CallResponse(**result)


@router.get("/calls/{session_id}", response_model=dict)
async def get_call_status(session_id: str):
    """Get call session status."""
    session = call_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return session.to_dict()


@router.post("/calls/{session_id}/end", response_model=CallResponse)
async def end_call(session_id: str):
    """End a call session."""
    result = await telephony.end_call(session_id)
    return CallResponse(**result)


@router.post("/calls/{session_id}/transfer", response_model=CallResponse)
async def transfer_call(session_id: str, target: str = Body(...)):
    """Transfer call to human."""
    result = await telephony.handle_call_transfer(session_id, target)
    return CallResponse(**result)


# ===== Voice Processing =====

@router.post("/transcribe", response_model=dict)
async def transcribe_audio(audio: bytes = Body(..., media_type="audio/wav")):
    """
    Transcribe audio to text.
    
    Accepts raw audio data and returns transcription.
    """
    text = await voice_service.transcribe_audio(audio)
    return {
        "text": text,
        "language": "en",
        "confidence": 0.95
    }


@router.post("/speak", response_model=dict)
async def generate_speech(text: str = Body(...), voice: Optional[str] = None):
    """
    Generate speech from text.
    
    Returns path to generated audio file.
    """
    audio_path = await voice_service.generate_speech(text, voice)
    if audio_path:
        return {
            "audio_url": f"/uploads/audio/{audio_path.name}",
            "voice": voice or settings.DEFAULT_VOICE
        }
    return {"error": "Speech generation failed"}


# ===== Agent Interaction =====

@router.post("/chat", response_model=dict)
async def chat_with_agent(
    message: str = Body(...),
    session_id: Optional[str] = Body(None),
    business_slug: str = Body("demo")
):
    """
    Chat with AI agent (text mode for testing).
    
    Returns AI response and any tool calls made.
    """
    # Get or create session
    if not session_id:
        session_id = f"web_{__import__('uuid').uuid4().hex[:8]}"
    
    result = await agent.get_response(
        session_id=session_id,
        user_message=message,
        db_session=None,
        business=None,
        caller_number=None
    )
    
    return {
        "session_id": session_id,
        "response": result.get("text", ""),
        "tools_called": result.get("tools_called", []),
        "should_transfer": result.get("should_transfer", False)
    }
