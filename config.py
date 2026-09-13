"""
Configuration management
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Bot Configuration
    BOT_TOKEN: str = ""
    
    # Ollama Configuration
    OLLAMA_MODEL: str = "qwen2.5:3b"
    OLLAMA_HOST: str = "http://localhost:11434"
    
    # Voice Configuration
    ENABLE_TTS: bool = True
    DEFAULT_VOICE: str = "en-US-GuyNeural"
    ACCENT_MODE: str = "american"  # american, british, indian, etc.
    
    # Database
    DATABASE_URL: str = "sqlite:///./agent_data.db"
    
    # Audio directory
    AUDIO_DIR: str = "./audio"
    
    # Premium features
    PREMIUM_MODES: list = ["bf_gf", "custom"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def load_settings() -> Settings:
    """Load settings from environment or defaults."""
    return Settings()


# Create singleton instance
settings = load_settings()

# Ensure audio directory exists
os.makedirs(settings.AUDIO_DIR, exist_ok=True)
