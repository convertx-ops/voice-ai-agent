"""
Voice Processing - Speech-to-Text and Text-to-Speech
"""
import os
import base64
import asyncio
import logging
from pathlib import Path
from typing import Optional

import numpy as np
from faster_whisper import WhisperModel
import edge_tts
import asyncio

from config import settings

logger = logging.getLogger(__name__)

# Initialize Whisper model (runs locally, no API costs)
whisper_model = None

def load_whisper_model():
    """Load Whisper model for speech recognition."""
    global whisper_model
    if whisper_model is None:
        logger.info("Loading Whisper model...")
        # Use medium or small for better balance of speed/accuracy
        whisper_model = WhisperModel(
            "medium",
            device="cpu",
            compute_type="int8"  # Quantized for CPU efficiency
        )
        logger.info("Whisper model loaded successfully")
    return whisper_model


async def transcribe_audio(audio_data: bytes) -> str:
    """
    Transcribe audio data to text.
    
    Args:
        audio_data: Raw audio bytes (should be WAV format, 16kHz mono)
    
    Returns:
        Transcribed text
    """
    try:
        model = load_whisper_model()
        
        # Save audio temporarily
        temp_dir = Path("./temp_audio")
        temp_dir.mkdir(exist_ok=True)
        
        audio_path = temp_dir / f"input_{int(asyncio.get_event_loop().time() * 1000)}.wav"
        with open(audio_path, 'wb') as f:
            f.write(audio_data)
        
        # Transcribe
        segments, info = model.transcribe(
            str(audio_path),
            beam_size=5,
            language="en",
            initial_prompt="Transcribe the following speech:"
        )
        
        text = "".join(segment.text for segment in segments)
        
        # Clean up
        audio_path.unlink(missing_ok=True)
        
        logger.info(f"Transcription: {text[:100]}...")
        return text.strip()
        
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        return "I didn't catch that. Could you please repeat?"


async def generate_speech(text: str, user_id: str, mode: str = None) -> Optional[str]:
    """
    Generate speech from text using Edge TTS (free, high quality).
    
    Args:
        text: Text to convert to speech
        user_id: User identifier for file naming
        mode: Conversation mode
    
    Returns:
        Path to generated audio file, or None if failed
    """
    try:
        # Select voice based on accent preference
        voices = {
            "american": "en-US-GuyNeural",      # Male, American
            "british": "en-GB-RyanNeural",       # Male, British
            "indian": "en-IN-PrabhatNeural",     # Male, Indian
            "female_us": "en-US-JennyNeural",    # Female, American
            "female_uk": "en-GB-LibbyNeural",    # Female, British
        }
        
        voice = voices.get(settings.ACCENT_MODE, voices["american"])
        
        # Create output directory
        output_dir = Path(settings.AUDIO_DIR) / user_id
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        timestamp = int(asyncio.get_event_loop().time() * 1000)
        audio_path = output_dir / f"response_{timestamp}.mp3"
        
        # Generate speech
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(str(audio_path))
        
        logger.info(f"Generated speech: {audio_path}")
        return str(audio_path)
        
    except Exception as e:
        logger.error(f"Speech generation error: {e}")
        return None


def download_voice_models():
    """Download necessary voice models (for first-time setup)."""
    import subprocess
    
    logger.info("Downloading voice models...")
    
    # Install Piper TTS if needed
    try:
        import piper
        logger.info("Piper TTS available")
    except ImportError:
        logger.warning("Piper TTS not installed, will use Edge TTS")
    
    logger.info("Voice models ready")


# Test function
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python voice.py <audio_file.wav>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    
    with open(audio_file, 'rb') as f:
        audio_data = f.read()
    
    async def test():
        text = await transcribe_audio(audio_data)
        print(f"\nTranscribed: {text}\n")
        
        audio_path = await generate_speech(text, "test_user")
        print(f"Generated audio: {audio_path}")
    
    asyncio.run(test())
