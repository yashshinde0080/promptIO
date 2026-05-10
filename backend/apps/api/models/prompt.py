from sqlalchemy import (
    Column, String, Boolean, DateTime, 
    ForeignKey, Enum, Text, Integer, 
    Float, JSON, Index
)
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import uuid
import enum


class PromptFramework(str, enum.Enum):
    STANDARD = "standard"
    REASONING = "reasoning"
    RACE = "race"
    CARE = "care"
    APE = "ape"
    CREATE = "create"
    TAG = "tag"
    CREO = "creo"
    RISE = "rise"
    PAIN = "pain"
    COAST = "coast"
    ROSES = "roses"
    RESEE = "resee"


class PromptVisibility(str, enum.Enum):
    PRIVATE = "private"
    TEAM = "team"
    ORGANIZATION = "organization"
    PUBLIC = "public"


class PromptStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"


class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False, index=True)
    description = Column(Text, nullable=True)
    original_content = Column(Text, nullable=False)
    optimized_content = Column(Text, nullable=True)
    framework = Column(Enum(PromptFramework), nullable=False)
    framework_data = Column(JSON, default=dict)
    variables = Column(JSON, default=list)
    tags = Column(JSON, default=list)
    status = Column(Enum(PromptStatus), default=PromptStatus.DRAFT)
    visibility = Column(Enum(PromptVisibility), default=PromptVisibility.PRIVATE)
    version = Column(Integer, default=1)
    is_template = Column(Boolean, default=False)
    is_pinned = Column(Boolean, default=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("prompts.id"), nullable=True)
    
    # Analytics
    total_runs = Column(Integer, default=0)
    avg_quality_score = Column(Float, default=0.0)
    avg_latency_ms = Column(Float, default=0.0)
    total_tokens_used = Column(Integer, default=0)
    total_cost_usd = Column(Float, default=0.0)
    
    # Compliance
    pii_detected = Column(Boolean, default=False)
    safety_score = Column(Float, default=1.0)
    compliance_flags = Column(JSON, default=list)
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    
    # Metadata
    search_vector = Column(TSVECTOR, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    owner = relationship("User", back_populates="prompts", foreign_keys=[owner_id])
    organization = relationship("Organization", back_populates="prompts")
    versions = relationship("PromptVersion", back_populates="prompt", lazy="dynamic")
    evaluations = relationship("Evaluation", back_populates="prompt", lazy="dynamic")
    ai_runs = relationship("AIRun", back_populates="prompt", lazy="dynamic")
    children = relationship("Prompt", foreign_keys=[parent_id], lazy="dynamic")

    __table_args__ = (
        Index("ix_prompts_search_vector", "search_vector", postgresql_using="gin"),
        Index("ix_prompts_owner_framework", "owner_id", "framework"),
        Index("ix_prompts_org_status", "organization_id", "status"),
    )

    def __repr__(self):
        return f"<Prompt {self.title}>"


class PromptVersion(Base):
    __tablename__ = "prompt_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prompt_id = Column(UUID(as_uuid=True), ForeignKey("prompts.id"), nullable=False)
    version = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    optimized_content = Column(Text, nullable=True)
    framework_data = Column(JSON, default=dict)
    change_summary = Column(Text, nullable=True)
    change_type = Column(String(50), nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    prompt = relationship("Prompt", back_populates="versions")
    created_by_user = relationship("User", foreign_keys=[created_by])

    def __repr__(self):
        return f"<PromptVersion {self.prompt_id} v{self.version}>"