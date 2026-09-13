"""Telephony service for handling phone calls via Twilio/Telnyx."""
import logging
import asyncio
from typing import Optional, Dict, Any, Callable
from datetime import datetime
import httpx

from app.services.call_session import CallSession, call_manager
from app.services.voice import voice_service
from app.services.agent import agent
from app.models.database import Business, Call, CallEvent
from config import settings

logger = logging.getLogger(__name__)


class TelephonyService:
    """
    Service for handling telephony operations.
    
    Supports:
    - Twilio (primary)
    - Telnyx (fallback)
    """
    
    def __init__(self):
        self.provider = None
        self.client = None
        self._init_provider()
    
    def _init_provider(self):
        """Initialize telephony provider."""
        if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
            self.provider = "twilio"
            self.account_sid = settings.TWILIO_ACCOUNT_SID
            self.auth_token = settings.TWILIO_AUTH_TOKEN
            self.phone_number = settings.TWILIO_PHONE_NUMBER
            logger.info("Initialized Twilio provider")
        elif settings.TELNYX_API_KEY:
            self.provider = "telnyx"
            self.api_key = settings.TELNYX_API_KEY
            self.phone_number = settings.TELNYX_PHONE_NUMBER
            logger.info("Initialized Telnyx provider")
        else:
            logger.warning("No telephony provider configured - voice demo mode only")
    
    async def handle_incoming_call(self, 
                                    caller_number: str, 
                                    business_slug: str,
                                    call_sid: str) -> Dict[str, Any]:
        """
        Handle an incoming call.
        
        Returns TwiML instructions for the telephony provider.
        """
        # Find business by slug
        # Note: In production, this would query database
        # For now, return demo response
        
        logger.info(f"Incoming call from {caller_number} for business {business_slug}")
        
        # Create call session
        try:
            session = call_manager.create_session(
                business_id=1,  # Would come from DB lookup
                caller_number=caller_number
            )
            
            # Start background processing
            asyncio.create_task(self._process_call(session, call_sid))
            
            return {
                "status": "accepted",
                "session_id": session.session_id,
                "message": "Call connected to AI receptionist"
            }
            
        except Exception as e:
            logger.error(f"Failed to handle incoming call: {e}")
            return {
                "status": "error",
                "message": "Failed to connect call"
            }
    
    async def _process_call(self, session: CallSession, call_sid: str):
        """Process a call session."""
        session.update_status(CallStatus.ACTIVE)
        
        try:
            # Initialize call in database
            db_call = Call(
                business_id=session.business_id,
                caller_number=session.caller_number,
                call_type="incoming",
                status="connected"
            )
            
            # Add initial event
            event = CallEvent(
                call_id=db_call.id if hasattr(db_call, 'id') else 0,
                sequence=1,
                event_type="call_started",
                role="system",
                content=f"Call started from {session.caller_number}"
            )
            
            # Process conversation loop
            await self._conversation_loop(session)
            
            # Mark complete
            session.finish(
                outcome=session.outcome or "completed",
                summary=session.ai_summary
            )
            db_call.status = "completed"
            db_call.duration_seconds = session.duration_seconds
            db_call.recording_url = None  # Would get from provider
            db_call.transcript = session.transcript
            db_call.ai_summary = session.ai_summary
            
        except Exception as e:
            logger.error(f"Call processing error: {e}")
            session.update_status(CallStatus.FAILED)
            session.finish("failed", f"Error: {str(e)}")
        
        finally:
            # Cleanup
            call_manager.remove_session(session.session_id)
    
    async def _conversation_loop(self, session: CallSession):
        """Main conversation loop for a call."""
        max_turns = 20  # Prevent infinite loops
        turn_count = 0
        
        while turn_count < max_turns and not session._cancel_event.is_set():
            turn_count += 1
            session.update_status(CallStatus.ACTIVE)
            
            # Wait for caller speech
            # In real implementation, this would stream audio from telephony provider
            logger.info(f"Call {session.session_id}: Waiting for caller speech (turn {turn_count})")
            
            # Simulate getting audio (in production, this comes from WebRTC/stream)
            caller_speech = await self._get_caller_speech(session)
            
            if not caller_speech or session._cancel_event.is_set():
                break
            
            # Add to transcript
            session.add_message("caller", caller_speech)
            
            # Get AI response
            response = await agent.get_response(
                session_id=session.session_id,
                user_message=caller_speech,
                db_session=None,  # Would be real DB session
                business=None,   # Would be real Business object
                caller_number=session.caller_number
            )
            
            # Add AI response to transcript
            session.add_message("assistant", response.get("text", ""))
            
            # Record tool calls
            for tool_call in response.get("tools_called", []):
                session.add_tool_call(
                    tool_call.get("tool", ""),
                    tool_call.get("input", {}),
                    tool_call.get("output", {})
                )
            
            # Check if transfer needed
            if response.get("should_transfer"):
                session.need_transfer = True
                session.cancel("AI requested human transfer")
                break
            
            # Generate speech response
            audio_path = await voice_service.generate_speech(response.get("text", ""))
            if audio_path:
                session.response_audio = audio_path.read_bytes() if audio_path.exists() else None
            
            # Small delay between turns
            await asyncio.sleep(0.5)
    
    async def _get_caller_speech(self, session: CallSession) -> str:
        """
        Get speech from caller.
        
        In production, this would:
        1. Stream audio from telephony provider
        2. Continuously transcribe using streaming ASR
        3. Return complete utterance when silence detected
        """
        # Demo: simulate getting speech
        await asyncio.sleep(1)  # Simulate listening
        return "Hello, I'd like to book an appointment"
    
    async def handle_call_transfer(self, session_id: str, target_number: str):
        """Transfer call to human."""
        session = call_manager.get_session(session_id)
        if session:
            session.need_transfer = True
            logger.info(f"Transferring call {session_id} to {target_number}")
            return {"success": True, "target": target_number}
        return {"success": False, "error": "Session not found"}
    
    async def end_call(self, session_id: str):
        """End a call."""
        session = call_manager.get_session(session_id)
        if session:
            session.cancel("Call ended")
            call_manager.remove_session(session_id)
            return {"success": True}
        return {"success": False, "error": "Session not found"}


# Global telephony service
telephony = TelephonyService()