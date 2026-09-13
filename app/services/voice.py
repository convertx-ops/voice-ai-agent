"""Voice processing service - Speech-to-Text and Text-to-Speech."""
import asyncio
import logging
import os
import tempfile
from pathlib import Path
from typing import Optional, AsyncGenerator
import edge_tts
from faster_whisper import WhisperModel
from config import settings

logger = logging.getLogger(__name__)


class VoiceService:
    """Service for handling audio transcription and speech synthesis."""
    
    def __init__(self):
        self.whisper_model = None
        self._init_whisper()
    
    def _init_whisper(self):
        """Initialize Whisper model."""
        try:
            logger.info("Loading Whisper model...")
            self.whisper_model = WhisperModel(
                "base",  # Using base for speed, can upgrade to medium/large
                device="cpu",
                compute_type="int8"
            )
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
    
    async def transcribe_audio(self, audio_data: bytes, language: str = None) -> str:
        """
        Transcribe audio data to text.
        
        Args:
            audio_data: Raw audio bytes (WAV, MP3, OGG, etc.)
            language: Language code (default from settings)
        
        Returns:
            Transcribed text
        """
        if self.whisper_model is None:
            logger.error("Whisper model not initialized")
            return ""
        
        lang = language or settings.STT_LANGUAGE
        
        try:
            # Save to temp file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
                tmp.write(audio_data)
                tmp_path = tmp.name
            
            try:
                # Transcribe
                segments, info = self.whisper_model.transcribe(
                    tmp_path,
                    beam_size=5,
                    language=lang,
                    initial_prompt="Business phone call, clear speech."
                )
                
                text = "".join(segment.text for segment in segments)
                logger.info(f"Transcription: {text[:100]}...")
                return text.strip()
                
            finally:
                # Cleanup temp file
                os.unlink(tmp_path)
                
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            return ""
    
    async def generate_speech(self, text: str, voice: str = None) -> Optional[Path]:
        """
        Generate speech from text using Edge TTS.
        
        Args:
            text: Text to convert to speech
            voice: Voice to use (default from settings)
        
        Returns:
            Path to generated audio file
        """
        if not settings.ENABLE_TTS:
            return None
        
        try:
            selected_voice = voice or settings.DEFAULT_VOICE
            
            # Create output directory
            output_dir = Path(settings.AUDIO_DIR)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate unique filename
            import time
            audio_path = output_dir / f"speech_{int(time.time() * 1000)}.mp3"
            
            # Generate speech
            communicate = edge_tts.Communicate(text, selected_voice)
            await communicate.save(str(audio_path))
            
            logger.info(f"Generated speech: {audio_path}")
            return audio_path
            
        except Exception as e:
            logger.error(f"Speech generation error: {e}")
            return None
    
    async def generate_streaming_speech(self, text: str, voice: str = None) -> AsyncGenerator[bytes, None]:
        """
        Generate streaming speech chunks.
        
        Args:
            text: Text to convert to speech
            voice: Voice to use
        
        Yields:
            Audio chunks
        """
        try:
            selected_voice = voice or settings.DEFAULT_VOICE
            communicate = edge_tts.Communicate(text, selected_voice)
            
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    yield chunk["data"]
                    
        except Exception as e:
            logger.error(f"Streaming speech error: {e}")
    
    async def detect_silence(self, audio_data: bytes, threshold: float = 0.1) -> bool:
        """Detect if audio contains silence (no meaningful speech)."""
        try:
            # Simple energy-based detection
            import numpy as np
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            energy = np.mean(np.abs(audio_array))
            return energy < threshold
        except Exception:
            return True  # Assume silence on error


# Singleton instance
voice_service = VoiceService()