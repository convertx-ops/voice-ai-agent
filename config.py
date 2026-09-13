"""Configuration for Voice + Brain System."""
from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Voice + Brain"
    VERSION: str = "1.0.0"
    
    # Ollama Configuration
    OLLAMA_MODEL: str = "qwen2.5:3b"
    OLLAMA_HOST: str = "http://localhost:11434"
    
    # Audio Configuration
    SAMPLE_RATE: int = 16000
    CHUNK_SIZE: int = 1024
    AUDIO_FORMAT: int = 2  # SIGFORMAT PCM
    
    # Whisper Configuration
    WHISPER_MODEL: str = "base"  # base, small, medium
    WHISPER_DEVICE: str = "cpu"
    WHISPER_COMPUTE_TYPE: str = "int8"
    WHISPER_LANGUAGE: str = "en"
    
    # TTS Configuration
    ENABLE_TTS: bool = True
    TTS_ENGINE: str = "piper"  # piper (local) or edge (online)
    PIPER_VOICE: str = "en_US-lessac-medium"  # Piper voice model name
    EDGE_VOICE: str = "en-IN-PrabhatNeural"  # Edge TTS Indian accent
    
    # Memory Configuration
    MEMORY_DIR: str = "./memory"
    MAX_CONTEXT_MESSAGES: int = 20
    
    # Recording Configuration
    RECORDINGS_DIR: str = "./recordings"
    AUDIO_DIR: str = "./audio"
    LOGS_DIR: str = "./logs"
    
    # Performance
    SILENCE_THRESHOLD: float = 0.5  # Seconds of silence to end recording
    MAX_RECORDING_DURATION: int = 60  # Maximum seconds per recording
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()

# Ensure directories exist
for dir_path in [settings.MEMORY_DIR, settings.RECORDINGS_DIR, 
                 settings.AUDIO_DIR, settings.LOGS_DIR]:
    os.makedirs(dir_path, exist_ok=True)