"""Voice Output - Text-to-Speech and Audio Playback."""
import asyncio
import logging
import tempfile
from pathlib import Path
from typing import Optional
import numpy as np
import sounddevice as sd
import soundfile as sf

from config import settings

logger = logging.getLogger(__name__)


class TextToSpeech:
    """Converts text to speech."""
    
    def __init__(self):
        self.engine = settings.TTS_ENGINE
        self.audio_buffer = None
    
    def generate_speech(self, text: str) -> Optional[Path]:
        """Generate speech from text."""
        try:
            if self.engine == "piper":
                return self._generate_piper(text)
            else:
                return self._generate_edge(text)
        except Exception as e:
            logger.error(f"TTS generation failed: {e}")
            return None
    
    def _generate_piper(self, text: str) -> Optional[Path]:
        """Generate speech using Piper TTS (local/offline)."""
        try:
            import piper
            
            # Create output directory
            output_dir = Path(settings.AUDIO_DIR)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate unique filename
            import time
            audio_path = output_dir / f"output_{int(time.time() * 1000)}.wav"
            
            # Generate speech
            with piper.Piper(settings.PIPER_VOICE) as piper_speaker:
                piper_speaker.say(text, str(audio_path))
            
            logger.info(f"Generated speech: {audio_path}")
            return audio_path
            
        except ImportError:
            logger.warning("Piper not installed, falling back to Edge TTS")
            return self._generate_edge(text)
        except Exception as e:
            logger.error(f"Piper TTS failed: {e}")
            return None
    
    def _generate_edge(self, text: str) -> Optional[Path]:
        """Generate speech using Edge TTS (online/free)."""
        try:
            import edge_tts
            
            # Create output directory
            output_dir = Path(settings.AUDIO_DIR)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate unique filename
            import time
            audio_path = output_dir / f"output_{int(time.time() * 1000)}.mp3"
            
            # Generate speech
            communicate = edge_tts.Communicate(text, settings.EDGE_VOICE)
            asyncio.run(communicate.save(str(audio_path)))
            
            logger.info(f"Generated speech: {audio_path}")
            return audio_path
            
        except Exception as e:
            logger.error(f"Edge TTS failed: {e}")
            return None
    
    def text_to_speech_path(self, text: str) -> Optional[str]:
        """Get path to generated speech file."""
        path = self.generate_speech(text)
        return str(path) if path else None


class AudioPlayer:
    """Plays audio files."""
    
    def __init__(self):
        self.is_playing = False
    
    def play_audio(self, audio_path: str) -> bool:
        """Play an audio file."""
        try:
            if not Path(audio_path).exists():
                logger.error(f"Audio file not found: {audio_path}")
                return False
            
            logger.info(f"Playing audio: {audio_path}")
            
            # Load and play audio
            audio_data, sample_rate = sf.read(audio_path)
            
            # Play audio
            sd.play(audio_data, sample_rate)
            sd.wait()
            
            logger.info("Audio playback complete")
            return True
            
        except Exception as e:
            logger.error(f"Audio playback failed: {e}")
            return False
    
    def play_text(self, text: str) -> bool:
        """Convert text to speech and play it."""
        tts = TextToSpeech()
        audio_path = tts.generate_speech(text)
        
        if audio_path:
            return self.play_audio(str(audio_path))
        
        return False


class VoiceOutput:
    """Main voice output class."""
    
    def __init__(self):
        self.tts = TextToSpeech()
        self.player = AudioPlayer()
    
    def speak(self, text: str) -> bool:
        """Speak text using TTS."""
        if not settings.ENABLE_TTS:
            logger.info("TTS disabled, skipping speech")
            return True
        
        return self.player.play_text(text)
    
    def speak_file(self, audio_path: str) -> bool:
        """Play an audio file."""
        return self.player.play_audio(audio_path)
    
    def say(self, text: str) -> str:
        """Speak text and return confirmation."""
        success = self.speak(text)
        return "Speaking..." if success else "Speech failed"


# Singleton instance
voice_output = VoiceOutput()