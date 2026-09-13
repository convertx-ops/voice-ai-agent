"""Voice Input - Microphone Recording and Speech Recognition."""
import asyncio
import logging
import wave
import tempfile
from pathlib import Path
from typing import Optional, Generator, Tuple
import numpy as np
import sounddevice as sd
import soundfile as sf
from faster_whisper import WhisperModel

from config import settings

logger = logging.getLogger(__name__)


class AudioRecorder:
    """Records audio from microphone."""
    
    def __init__(self):
        self.sample_rate = settings.SAMPLE_RATE
        self.channels = 1  # Mono
        self.recording = False
        self.audio_data = []
        self.stream = None
    
    def start_recording(self) -> bool:
        """Start recording from microphone."""
        try:
            self.audio_data = []
            self.recording = True
            
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype='int16',
                callback=self._audio_callback
            )
            self.stream.start()
            logger.info("Recording started")
            return True
        except Exception as e:
            logger.error(f"Failed to start recording: {e}")
            return False
    
    def stop_recording(self) -> bytes:
        """Stop recording and return audio data."""
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.recording = False
            logger.info("Recording stopped")
        
        # Convert to WAV format
        return self._encode_wav()
    
    def _audio_callback(self, indata, frames, time, status):
        """Callback for audio stream."""
        if status:
            logger.warning(f"Audio callback status: {status}")
        self.audio_data.append(indata.copy())
    
    def _encode_wav(self) -> bytes:
        """Encode audio data to WAV format."""
        if not self.audio_data:
            return b''
        
        audio_array = np.concatenate(self.audio_data, axis=0)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            sf.write(tmp.name, audio_array, self.sample_rate, format='WAV', subtype='PCM_16')
            tmp_path = tmp.name
        
        # Read the WAV file
        with open(tmp_path, 'rb') as f:
            wav_data = f.read()
        
        # Clean up temp file
        Path(tmp_path).unlink(missing_ok=True)
        
        return wav_data
    
    def detect_silence(self, audio_array: np.ndarray, threshold: float = 0.01) -> bool:
        """Check if audio contains mostly silence."""
        if len(audio_array) == 0:
            return True
        rms = np.sqrt(np.mean(audio_array.astype(float) ** 2))
        return rms < threshold


class SpeechRecognizer:
    """Transcribes audio using Whisper."""
    
    def __init__(self):
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load Whisper model."""
        try:
            logger.info(f"Loading Whisper model: {settings.WHISPER_MODEL}")
            self.model = WhisperModel(
                settings.WHISPER_MODEL,
                device=settings.WHISPER_DEVICE,
                compute_type=settings.WHISPER_COMPUTE_TYPE
            )
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            raise
    
    def transcribe(self, audio_path: str) -> str:
        """Transcribe audio file to text."""
        if not self.model:
            return ""
        
        try:
            segments, info = self.model.transcribe(
                audio_path,
                beam_size=5,
                language=settings.WHISPER_LANGUAGE,
                initial_prompt="Transcribe this speech clearly."
            )
            
            text = "".join(segment.text for segment in segments)
            logger.info(f"Transcription: {text[:100]}...")
            return text.strip()
            
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            return ""
    
    def transcribe_bytes(self, wav_data: bytes) -> str:
        """Transcribe raw WAV bytes to text."""
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmp.write(wav_data)
            tmp_path = tmp.name
        
        try:
            return self.transcribe(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)


class VoiceInput:
    """Main voice input class combining recording and transcription."""
    
    def __init__(self):
        self.recorder = AudioRecorder()
        self.recognizer = SpeechRecognizer()
    
    def record_and_transcribe(self, max_duration: int = 30) -> Tuple[str, bool]:
        """
        Record from microphone and transcribe.
        
        Returns:
            (transcribed_text, success)
        """
        logger.info("Starting recording...")
        
        if not self.recorder.start_recording():
            return "", False
        
        # Record for specified duration
        import time
        start_time = time.time()
        
        while time.time() - start_time < max_duration:
            # Check for silence (simple implementation)
            time.sleep(0.1)
        
        # Stop recording
        wav_data = self.recorder.stop_recording()
        
        if not wav_data:
            logger.warning("No audio recorded")
            return "", False
        
        # Transcribe
        text = self.recognizer.transcribe_bytes(wav_data)
        
        if not text:
            logger.warning("Empty transcription")
            return "", False
        
        logger.info(f"Transcribed: {text}")
        return text, True
    
    def record_to_file(self, filename: str) -> str:
        """Record to a specific file path."""
        if not self.recorder.start_recording():
            return ""
        
        import time
        time.sleep(10)  # Record for 10 seconds
        
        wav_data = self.recorder.stop_recording()
        
        # Save to file
        output_path = Path(settings.RECORDINGS_DIR) / f"{filename}.wav"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(wav_data)
        
        return str(output_path)


# Singleton instance
voice_input = VoiceInput()