from sqlalchemy import Column, String, DateTime, ForeignKey, Float, Integer, JSON, Text, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import uuid
import enum


class AIRunStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AIRun(Base):
    __tablename__ = "ai_runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prompt_id = Column(UUID(as_uuid=True), ForeignKey("prompts.id"), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True)
    
    # Request
    input_prompt = Column(Text, nullable=False)
    model = Column(String(200), nullable=False)
    provider = Column(String(100), nullable=True)
    framework = Column(String(50), nullable=True)
    parameters = Column(JSON, default=dict)
    
    # Response
    response = Column(Text, nullable=True)
    status = Column(Enum(AIRunStatus), default=AIRunStatus.PENDING)
    
    # Performance
    latency_ms = Column(Float, nullable=True)
    input_tokens = Column(Integer, nullable=True)
    output_tokens = Column(Integer, nullable=True)
    total_tokens = Column(Integer, nullable=True)
    cost_usd = Column(Float, nullable=True)
    
    # Streaming
    is_streaming = Column(Boolean, default=False)
    
    # Error Handling
    error_message = Column(Text, nullable=True)
    error_code = Column(String(100), nullable=True)
    retry_count = Column(Integer, default=0)
    
    # Metadata
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    prompt = relationship("Prompt", back_populates="ai_runs")
    user = relationship("User", back_populates="ai_runs")

    def __repr__(self):
        return f"<AIRun {self.id}>"