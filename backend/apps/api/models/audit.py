from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import uuid
import enum


class AuditAction(str, enum.Enum):
    # Auth
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    USER_REGISTER = "user_register"
    PASSWORD_CHANGE = "password_change"
    MFA_ENABLED = "mfa_enabled"
    
    # Prompts
    PROMPT_CREATE = "prompt_create"
    PROMPT_UPDATE = "prompt_update"
    PROMPT_DELETE = "prompt_delete"
    PROMPT_OPTIMIZE = "prompt_optimize"
    PROMPT_EXPORT = "prompt_export"
    PROMPT_APPROVE = "prompt_approve"
    PROMPT_REJECT = "prompt_reject"
    
    # AI
    AI_RUN_EXECUTE = "ai_run_execute"
    AI_MODEL_CHANGE = "ai_model_change"
    
    # Admin
    USER_CREATE = "user_create"
    USER_UPDATE = "user_update"
    USER_SUSPEND = "user_suspend"
    ROLE_CHANGE = "role_change"
    ORG_SETTINGS_CHANGE = "org_settings_change"
    
    # Security
    SECURITY_VIOLATION = "security_violation"
    PII_DETECTED = "pii_detected"
    COMPLIANCE_VIOLATION = "compliance_violation"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    INJECTION_DETECTED = "injection_detected"


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True)
    action = Column(Enum(AuditAction), nullable=False)
    resource_type = Column(String(100), nullable=True)
    resource_id = Column(String(255), nullable=True)
    details = Column(JSON, default=dict)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    status = Column(String(50), default="success")
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog {self.action} by {self.user_id}>"