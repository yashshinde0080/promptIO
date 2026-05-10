from sqlalchemy import Column, String, Boolean, DateTime, Enum, Text, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import uuid
import enum


class PlanType(str, enum.Enum):
    FREE = "free"
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    GOVERNMENT = "government"


class ComplianceMode(str, enum.Enum):
    STANDARD = "standard"
    GDPR = "gdpr"
    FEDRAMP = "fedramp"
    GOVRAMP = "govramp"
    SOC2 = "soc2"


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    plan = Column(Enum(PlanType), default=PlanType.FREE, nullable=False)
    compliance_mode = Column(Enum(ComplianceMode), default=ComplianceMode.STANDARD)
    logo_url = Column(String(500), nullable=True)
    website = Column(String(500), nullable=True)
    max_users = Column(Integer, default=5)
    max_prompts = Column(Integer, default=100)
    max_api_calls_per_month = Column(Integer, default=1000)
    current_api_calls = Column(Integer, default=0)
    monthly_token_budget = Column(Integer, default=100000)
    used_tokens = Column(Integer, default=0)
    allowed_models = Column(JSON, default=list)
    settings = Column(JSON, default=dict)
    sso_enabled = Column(Boolean, default=False)
    sso_provider = Column(String(100), nullable=True)
    sso_config = Column(JSON, default=dict)
    is_active = Column(Boolean, default=True)
    trial_ends_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    users = relationship("User", back_populates="organization", lazy="dynamic")
    prompts = relationship("Prompt", back_populates="organization", lazy="dynamic")

    def __repr__(self):
        return f"<Organization {self.name}>"