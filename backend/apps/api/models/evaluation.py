from sqlalchemy import Column, String, DateTime, ForeignKey, Float, Integer, JSON, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import uuid
import enum


class EvaluationStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prompt_id = Column(UUID(as_uuid=True), ForeignKey("prompts.id"), nullable=False)
    ai_run_id = Column(UUID(as_uuid=True), ForeignKey("ai_runs.id"), nullable=True)
    status = Column(Enum(EvaluationStatus), default=EvaluationStatus.PENDING)
    model_used = Column(String(100), nullable=True)
    
    # Core Metrics
    relevance_score = Column(Float, nullable=True)       # 0-1
    accuracy_score = Column(Float, nullable=True)         # 0-1
    clarity_score = Column(Float, nullable=True)          # 0-1
    specificity_score = Column(Float, nullable=True)      # 0-1
    safety_score = Column(Float, nullable=True)           # 0-1
    reasoning_depth_score = Column(Float, nullable=True)  # 0-1
    overall_quality_score = Column(Float, nullable=True)  # 0-1 (weighted average)
    
    # Performance Metrics
    latency_ms = Column(Float, nullable=True)
    token_count_input = Column(Integer, nullable=True)
    token_count_output = Column(Integer, nullable=True)
    total_tokens = Column(Integer, nullable=True)
    estimated_cost_usd = Column(Float, nullable=True)
    
    # AI Analysis
    hallucination_risk = Column(Float, nullable=True)     # 0-1
    ambiguity_score = Column(Float, nullable=True)        # 0-1
    complexity_score = Column(Float, nullable=True)       # 0-1
    intent_clarity = Column(Float, nullable=True)         # 0-1
    
    # Detailed Results
    strengths = Column(JSON, default=list)
    weaknesses = Column(JSON, default=list)
    suggestions = Column(JSON, default=list)
    detailed_feedback = Column(Text, nullable=True)
    
    # Compliance
    pii_detected = Column(JSON, default=list)
    toxicity_score = Column(Float, nullable=True)
    bias_detected = Column(JSON, default=list)
    compliance_issues = Column(JSON, default=list)
    
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    prompt = relationship("Prompt", back_populates="evaluations")
    ai_run = relationship("AIRun", foreign_keys=[ai_run_id])

    def __repr__(self):
        return f"<Evaluation {self.id}>"