"""Security utilities for authentication and authorization."""
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
import hashlib
import secrets

from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password for storing."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


def generate_api_key() -> tuple[str, str]:
    """Generate a new API key and return (raw_key, prefix)."""
    raw_key = f"cvx_{secrets.token_hex(32)}"
    prefix = raw_key[:16]  # Show first 16 chars
    return raw_key, prefix


def hash_api_key(raw_key: str) -> str:
    """Hash API key for storage."""
    return hashlib.sha256(raw_key.encode()).hexdigest()


def verify_api_key(stored_hash: str, provided_key: str) -> bool:
    """Verify an API key against its stored hash."""
    return hashlib.sha256(provided_key.encode()).hexdigest() == stored_hash