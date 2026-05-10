from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from models.audit import AuditLog, AuditAction
from config import settings
import structlog

logger = structlog.get_logger(__name__)


class AuditService:
    """
    Enterprise audit logging service
    Compliant with GDPR, FedRAMP, GovRAMP requirements
    """

    async def log(
        self,
        db: AsyncSession,
        action: AuditAction,
        user_id: Optional[str] = None,
        organization_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        status: str = "success",
        error_message: Optional[str] = None,
    ) -> None:
        if not settings.AUDIT_LOG_ENABLED:
            return

        try:
            log_entry = AuditLog(
                user_id=user_id,
                organization_id=organization_id,
                action=action,
                resource_type=resource_type,
                resource_id=str(resource_id) if resource_id else None,
                details=details or {},
                ip_address=ip_address,
                user_agent=user_agent,
                status=status,
                error_message=error_message,
            )
            db.add(log_entry)
            # Don't commit here - let the request lifecycle handle it

            logger.info(
                "Audit log created",
                action=action.value,
                user_id=str(user_id) if user_id else None,
                resource_type=resource_type,
                status=status,
            )
        except Exception as e:
            # Audit logging should never break the main flow
            logger.error("Failed to create audit log", error=str(e), action=action.value)


audit_service = AuditService()