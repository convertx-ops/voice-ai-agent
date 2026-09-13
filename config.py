from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    # App
    APP_NAME: str = "ConvertX Voice Agent"
    DEBUG: bool = False
    VERSION: str = "2.0.0"
    
    # Telephony
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None
    TELNYX_API_KEY: Optional[str] = None
    TELNYX_PHONE_NUMBER: Optional[str] = None
    
    # AI/LLM
    OLLAMA_MODEL: str = "qwen2.5:3b"
    OLLAMA_HOST: str = "http://localhost:11434"
    OPENAI_API_KEY: Optional[str] = None  # For fallback
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # Voice
    ENABLE_TTS: bool = True
    DEFAULT_VOICE: str = "en-IN-PrabhatNeural"  # Indian accent
    ACCENT_MODE: str = "indian"
    STT_LANGUAGE: str = "en"
    
    # Database
    DATABASE_URL: str = "sqlite:///./data/voice_agent.db"
    # Production: postgresql+asyncpg://user:pass@host:port/dbname
    
    # Security
    SECRET_KEY: str = "change-me-in-production-use-random-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # API Keys
    JWT_SECRET_KEY: str = "jwt-secret-change-in-production"
    
    # Paths
    AUDIO_DIR: str = "./uploads/audio"
    RECORDINGS_DIR: str = "./recordings"
    LOGS_DIR: str = "./logs"
    
    # Rate Limiting
    RATE_LIMIT_CALLS_PER_MINUTE: int = 10
    RATE_LIMIT_TOKENS_PER_MINUTE: int = 100
    
    # Business
    MAX_CONCURRENT_CALLS: int = 100
    CALL_TIMEOUT_SECONDS: int = 300  # 5 minutes max
    SILENCE_TIMEOUT_SECONDS: int = 10
    
    # Notifications
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    ADMIN_TELEGRAM_ID: Optional[int] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()

# Ensure directories exist
os.makedirs(settings.AUDIO_DIR, exist_ok=True)
os.makedirs(settings.RECORDINGS_DIR, exist_ok=True)
os.makedirs(settings.LOGS_DIR, exist_ok=True)
