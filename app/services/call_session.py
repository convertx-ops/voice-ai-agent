"""Call session management for handling concurrent calls."""
import asyncio
import logging
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, Callable
from enum import Enum
import threading

logger = logging.getLogger(__name__)


class CallStatus(Enum):
    """Status of an active call."""
    INITIALIZING = "initializing"
    CONNECTING = "connecting"
    ACTIVE = "active"
    TRANSFERRING = "transferring"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMED_OUT = "timed_out"


class CallSession:
    """
    Manages the state of a single phone call session.
    
    Handles:
    - Session lifecycle
    - Audio streaming
    - Conversation history
    - Tool execution tracking
    """
    
    def __init__(self, session_id: str, business_id: int, caller_number: str):
        self.session_id = session_id
        self.business_id = business_id
        self.caller_number = caller_number
        self.status = CallStatus.INITIALIZING
        self.started_at = datetime.utcnow()
        self.ended_at: Optional[datetime] = None
        self.duration_seconds = 0
        
        # Conversation
        self.messages: list = []  # [user, assistant] exchanges
        self.tool_calls: list = []
        self.transcript: str = ""
        
        # Results
        self.outcome: Optional[str] = None
        self.ai_summary: Optional[str] = None
        self.need_transfer: bool = False
        self.appointment_id: Optional[int] = None
        self.lead_id: Optional[int] = None
        
        # Audio
        self.audio_chunks: list = []
        self.response_audio: Optional[bytes] = None
        
        # Cancellation
        self._cancel_event = asyncio.Event()
        self._task: Optional[asyncio.Task] = None
    
    def update_status(self, new_status: CallStatus):
        """Update call status."""
        old_status = self.status
        self.status = new_status
        logger.info(f"Call {self.session_id}: {old_status.value} -> {new_status.value}")
    
    def add_message(self, role: str, content: str):
        """Add a message to conversation."""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.transcript += f"{role}: {content}\n"
    
    def add_tool_call(self, tool_name: str, input_data: dict, output: dict):
        """Record a tool call."""
        self.tool_calls.append({
            "tool": tool_name,
            "input": input_data,
            "output": output,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def finish(self, outcome: str, summary: str = None):
        """Mark call as complete."""
        self.ended_at = datetime.utcnow()
        self.duration_seconds = int((self.ended_at - self.started_at).total_seconds())
        self.outcome = outcome
        self.ai_summary = summary
        self.update_status(CallStatus.COMPLETED)
    
    def cancel(self, reason: str = "user_interrupted"):
        """Cancel the call."""
        self.need_transfer = True
        self.finish("transferred", f"Transferred due to: {reason}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize session to dictionary."""
        return {
            "session_id": self.session_id,
            "business_id": self.business_id,
            "caller_number": self.caller_number,
            "status": self.status.value,
            "started_at": self.started_at.isoformat(),
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
            "duration_seconds": self.duration_seconds,
            "outcome": self.outcome,
            "summary": self.ai_summary,
            "message_count": len(self.messages),
            "tool_calls_count": len(self.tool_calls),
            "need_transfer": self.need_transfer
        }


class CallManager:
    """Manages multiple concurrent call sessions."""
    
    def __init__(self, max_concurrent: int = 100):
        self.max_concurrent = max_concurrent
        self.sessions: Dict[str, CallSession] = {}
        self._lock = threading.Lock()
        self._active_count = 0
    
    def create_session(self, business_id: int, caller_number: str) -> CallSession:
        """Create a new call session."""
        session_id = str(uuid.uuid4())
        
        with self._lock:
            if self._active_count >= self.max_concurrent:
                raise RuntimeError("Maximum concurrent calls reached")
            self._active_count += 1
        
        session = CallSession(session_id, business_id, caller_number)
        self.sessions[session_id] = session
        
        logger.info(f"Created call session {session_id} for business {business_id}")
        return session
    
    def get_session(self, session_id: str) -> Optional[CallSession]:
        """Get a session by ID."""
        return self.sessions.get(session_id)
    
    def remove_session(self, session_id: str):
        """Remove a completed session."""
        with self._lock:
            self._active_count -= 1
        
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Removed session {session_id}")
    
    def get_active_count(self) -> int:
        """Get number of active sessions."""
        return self._active_count
    
    def cleanup_old_sessions(self, max_age_minutes: int = 60):
        """Remove sessions older than max_age_minutes that are completed."""
        import time
        now = time.time()
        to_remove = []
        
        for sid, session in self.sessions.items():
            if session.ended_at:
                age = now - session.ended_at.timestamp()
                if age > max_age_minutes * 60:
                    to_remove.append(sid)
        
        for sid in to_remove:
            self.remove_session(sid)
        
        if to_remove:
            logger.info(f"Cleaned up {len(to_remove)} old sessions")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get call statistics."""
        active = sum(1 for s in self.sessions.values() if s.status not in [CallStatus.COMPLETED, CallStatus.FAILED])
        return {
            "max_concurrent": self.max_concurrent,
            "active_calls": active,
            "total_sessions": len(self.sessions),
            "capacity_used_percent": (active / self.max_concurrent * 100) if self.max_concurrent > 0 else 0
        }


# Global call manager
call_manager = CallManager()