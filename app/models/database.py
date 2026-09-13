"""Core database models and SQLAlchemy setup."""
from datetime import datetime
from sqlalchemy import (
    create_engine, Column, Integer, String, Text, Boolean, 
    DateTime, ForeignKey, JSON, Float, UniqueConstraint, Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from typing import Optional, List, Dict, Any
import json

from config import settings

Base = declarative_base()


class User(Base):
    """Application user (business owner)."""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    phone = Column(String(50))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    subscription_tier = Column(String(50), default='free')  # free, starter, pro, enterprise
    subscription_expires = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    businesses = relationship("Business", back_populates="owner", cascade="all, delete-orphan")
    api_keys = relationship("ApiKey", back_populates="user", cascade="all, delete-orphan")
    calls = relationship("Call", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class Business(Base):
    """Business that uses the AI receptionist."""
    __tablename__ = 'businesses'
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text)
    timezone = Column(String(50), default='UTC')
    language = Column(String(10), default='en')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Configuration (JSON)
    business_config = Column(JSON, default={})
    
    # Relationships
    owner = relationship("User", back_populates="businesses")
    phone_numbers = relationship("PhoneNumber", back_populates="business", cascade="all, delete-orphan")
    services = relationship("Service", back_populates="business", cascade="all, delete-orphan")
    faqs = relationship("FAQ", back_populates="business", cascade="all, delete-orphan")
    calls = relationship("Call", back_populates="business", cascade="all, delete-orphan")
    leads = relationship("Lead", back_populates="business", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="business", cascade="all, delete-orphan")
    
    def get_config(self, key: str, default=None) -> Any:
        """Get a configuration value."""
        config = self.business_config or {}
        return config.get(key, default)
    
    def set_config(self, key: str, value: Any):
        """Set a configuration value."""
        if self.business_config is None:
            self.business_config = {}
        self.business_config[key] = value


class PhoneNumber(Base):
    """Phone number assigned to a business."""
    __tablename__ = 'phone_numbers'
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey('businesses.id'), nullable=False)
    number = Column(String(20), unique=True, index=True, nullable=False)
    provider = Column(String(50), nullable=False)  # twilio, telnyx
    inbound_enabled = Column(Boolean, default=True)
    outbound_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    business = relationship("Business", back_populates="phone_numbers")
    call_events = relationship("CallEvent", back_populates="phone_number")


class Service(Base):
    """Services offered by the business."""
    __tablename__ = 'services'
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey('businesses.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    duration_minutes = Column(Integer, default=30)
    price = Column(Float)
    price_currency = Column(String(3), default='INR')
    available = Column(Boolean, default=True)
    booking_required = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    business = relationship("Business", back_populates="services")


class FAQ(Base):
    """Frequently asked questions for the business."""
    __tablename__ = 'faqs'
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey('businesses.id'), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String(100))
    keywords = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    business = relationship("Business", back_populates="faqs")


class Call(Base):
    """Incoming/outgoing call record."""
    __tablename__ = 'calls'
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey('businesses.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    phone_number_id = Column(Integer, ForeignKey('phone_numbers.id'), nullable=True)
    
    # Call metadata
    caller_number = Column(String(20), nullable=False)
    call_type = Column(String(20), nullable=False)  # incoming, outgoing
    status = Column(String(50), default='queued')  # queued, ringing, connected, completed, failed, transferred
    duration_seconds = Column(Integer, default=0)
    
    # Recording
    recording_url = Column(String(500))
    transcript = Column(Text)
    
    # AI response
    ai_summary = Column(Text)
    outcome = Column(String(100))  # appointment_booked, lead_captured, transferred, etc.
    
    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    business = relationship("Business", back_populates="calls")
    user = relationship("User", back_populates="calls")
    events = relationship("CallEvent", back_populates="call", order_by="CallEvent.sequence")
    leads = relationship("Lead", back_populates="call", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="call", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Call(id={self.id}, caller={self.caller_number}, status={self.status})>"


class CallEvent(Base):
    """Individual events within a call (transcript segments, actions)."""
    __tablename__ = 'call_events'
    
    id = Column(Integer, primary_key=True, index=True)
    call_id = Column(Integer, ForeignKey('calls.id'), nullable=False)
    sequence = Column(Integer, nullable=False)
    event_type = Column(String(50), nullable=False)  # speech, transcription, ai_response, tool_call, etc.
    
    # Content
    role = Column(String(20))  # caller, assistant
    content = Column(Text)
    audio_url = Column(String(500))
    
    # Tool execution
    tool_name = Column(String(100))
    tool_input = Column(JSON)
    tool_output = Column(JSON)
    
    # Metadata
    confidence = Column(Float)
    duration_ms = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    call = relationship("Call", back_populates="events")
    
    def __repr__(self):
        return f"<CallEvent(id={self.id}, seq={self.sequence}, type={self.event_type})>"


class Lead(Base):
    """Captured lead from a call."""
    __tablename__ = 'leads'
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey('businesses.id'), nullable=False)
    call_id = Column(Integer, ForeignKey('calls.id'), nullable=True)
    
    # Lead info
    name = Column(String(255))
    phone_number = Column(String(20))
    email = Column(String(255))
    source = Column(String(100), default='phone_call')
    
    # Qualification
    qualification_score = Column(Integer)  # 0-100
    qualified = Column(Boolean, default=False)
    
    # Additional data
    notes = Column(Text)
    custom_fields = Column(JSON, default={})
    
    # Status
    status = Column(String(50), default='new')  # new, contacted, qualified, converted, lost
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    business = relationship("Business", back_populates="leads")
    call = relationship("Call", back_populates="leads")
    
    def __repr__(self):
        return f"<Lead(id={self.id}, name={self.name}, phone={self.phone_number})>"


class Appointment(Base):
    """Booked appointment."""
    __tablename__ = 'appointments'
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey('businesses.id'), nullable=False)
    call_id = Column(Integer, ForeignKey('calls.id'), nullable=True)
    lead_id = Column(Integer, ForeignKey('leads.id'), nullable=True)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=True)
    
    # Appointment details
    title = Column(String(255))
    description = Column(Text)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    
    # Customer info
    customer_name = Column(String(255))
    customer_phone = Column(String(20))
    customer_email = Column(String(255))
    
    # Status
    status = Column(String(50), default='confirmed')  # confirmed, cancelled, completed, no_show
    confirmation_sent = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    business = relationship("Business", back_populates="appointments")
    call = relationship("Call", back_populates="appointments")
    lead = relationship("Lead", back_populates=None)  # Added later if needed
    service = relationship("Service", back_populates=None)
    
    def __repr__(self):
        return f"<Appointment(id={self.id}, customer={self.customer_name}, time={self.start_time})>"


class ApiKey(Base):
    """API key for programmatic access."""
    __tablename__ = 'api_keys'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(255), nullable=False)
    key_hash = Column(String(255), unique=True, index=True, nullable=False)
    key_prefix = Column(String(20), nullable=False)  # Display part of key
    permissions = Column(JSON, default=list)  # ['read', 'write', 'admin']
    is_active = Column(Boolean, default=True)
    last_used_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="api_keys")
    
    def __repr__(self):
        return f"<ApiKey(id={self.id}, prefix={self.key_prefix})>"


class UsageRecord(Base):
    """Usage tracking for billing."""
    __tablename__ = 'usage_records'
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey('businesses.id'), nullable=False)
    record_date = Column(DateTime, nullable=False)
    
    # Metrics
    total_calls = Column(Integer, default=0)
    total_duration_seconds = Column(Integer, default=0)
    total_transcription_chars = Column(Integer, default=0)
    total_llm_tokens = Column(Integer, default=0)
    total_tts_characters = Column(Integer, default=0)
    
    # Costs (in cents)
    telephony_cost = Column(Float, default=0.0)
    stt_cost = Column(Float, default=0.0)
    llm_cost = Column(Float, default=0.0)
    tts_cost = Column(Float, default=0.0)
    total_cost = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    business = relationship("Business")
    
    __table_args__ = (
        UniqueConstraint('business_id', 'record_date', name='uq_business_date'),
        Index('idx_usage_date', 'record_date'),
    )
    
    def __repr__(self):
        return f"<UsageRecord(id={self.id}, business={self.business_id}, date={self.record_date})>"


# Database initialization
def get_engine(database_url: str = None):
    """Get SQLAlchemy engine."""
    url = database_url or settings.DATABASE_URL
    return create_engine(url, pool_pre_ping=True, echo=settings.DEBUG)


def get_session_factory(engine):
    """Get session factory."""
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_db():
    """Initialize database tables."""
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    return engine


def get_db():
    """Dependency for getting database session."""
    engine = get_engine()
    Session = get_session_factory(engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()