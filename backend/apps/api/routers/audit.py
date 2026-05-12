from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database import get_db
from dependencies import get_current_active_user
from models.user import User
from models.audit import AuditLog

router = APIRouter(prefix="/audit", tags=["Audit"])


@router.get("/logs")
async def get_audit_logs(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=50, ge=1, le=200),
    action: Optional[str] = Query(default=None),
    user_id: Optional[str] = Query(default=None),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get audit logs for current user (or all if admin)"""
    query = select(AuditLog).order_by(AuditLog.created_at.desc())

    # Non-admin users only see their own logs
    if current_user.role.value != "admin":
        query = query.where(AuditLog.user_id == str(current_user.id))

    if action:
        query = query.where(AuditLog.action == action)
    if user_id and current_user.role.value == "admin":
        query = query.where(AuditLog.user_id == user_id)

    count_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = count_result.scalar()

    query = query.offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)
    logs = result.scalars().all()

    return {
        "items": [
            {
                "id": str(log.id),
                "user_id": str(log.user_id) if log.user_id else None,
                "action": log.action.value,
                "resource_type": log.resource_type,
                "resource_id": log.resource_id,
                "details": log.details,
                "ip_address": log.ip_address,
                "status": log.status,
                "created_at": str(log.created_at),
            }
            for log in logs
        ],
        "total": total,
        "page": page,
        "per_page": per_page,
    }


@router.get("/export")
async def export_audit_logs(
    format: str = Query(default="json"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Export audit logs"""
    query = select(AuditLog).order_by(AuditLog.created_at.desc())

    if current_user.role.value != "admin":
        query = query.where(AuditLog.user_id == str(current_user.id))

    result = await db.execute(query.limit(1000))
    logs = result.scalars().all()

    items = [
        {
            "id": str(log.id),
            "user_id": str(log.user_id) if log.user_id else None,
            "action": log.action.value,
            "resource_type": log.resource_type,
            "resource_id": log.resource_id,
            "status": log.status,
            "created_at": str(log.created_at),
        }
        for log in logs
    ]

    if format == "csv":
        import csv
        import io
        from fastapi.responses import StreamingResponse

        output = io.StringIO()
        if items:
            writer = csv.DictWriter(output, fieldnames=items[0].keys())
            writer.writeheader()
            writer.writerows(items)

        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=audit_logs.csv"},
        )

    return {"items": items, "total": len(items)}
