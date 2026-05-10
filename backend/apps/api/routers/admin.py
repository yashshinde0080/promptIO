from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from database import get_db
from dependencies import require_admin
from models.user import User, UserRole, UserStatus
from models.audit import AuditLog
from schemas.user import UserAdminUpdateRequest
from typing import Optional

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users")
async def list_all_users(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    search: Optional[str] = Query(default=None),
    role: Optional[str] = Query(default=None),
    status_filter: Optional[str] = Query(default=None, alias="status"),
    current_user: User = Depends(require_admin()),
    db: AsyncSession = Depends(get_db),
):
    """List all users (admin only)"""
    query = select(User)

    if search:
        from sqlalchemy import or_
        query = query.where(
            or_(
                User.email.ilike(f"%{search}%"),
                User.username.ilike(f"%{search}%"),
                User.full_name.ilike(f"%{search}%"),
            )
        )
    if role:
        query = query.where(User.role == role)
    if status_filter:
        query = query.where(User.status == status_filter)

    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    query = query.offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)
    users = result.scalars().all()

    return {
        "items": [
            {
                "id": str(u.id),
                "email": u.email,
                "username": u.username,
                "full_name": u.full_name,
                "role": u.role.value,
                "status": u.status.value,
                "organization_id": str(u.organization_id) if u.organization_id else None,
                "login_count": u.login_count,
                "last_login_at": str(u.last_login_at) if u.last_login_at else None,
                "created_at": str(u.created_at),
            }
            for u in users
        ],
        "total": total,
        "page": page,
        "per_page": per_page,
    }


@router.put("/users/{user_id}")
async def update_user(
    user_id: str,
    data: UserAdminUpdateRequest,
    current_user: User = Depends(require_admin()),
    db: AsyncSession = Depends(get_db),
):
    """Update user role/status (admin only)"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    update_data = data.model_dump(exclude_none=True)
    if update_data:
        await db.execute(update(User).where(User.id == user_id).values(**update_data))

    return {"message": "User updated successfully", "user_id": user_id}


@router.get("/audit-logs")
async def get_audit_logs(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=50, ge=1, le=200),
    action: Optional[str] = Query(default=None),
    user_id: Optional[str] = Query(default=None),
    current_user: User = Depends(require_admin()),
    db: AsyncSession = Depends(get_db),
):
    """Get audit logs (admin only)"""
    query = select(AuditLog).order_by(AuditLog.created_at.desc())

    if action:
        query = query.where(AuditLog.action == action)
    if user_id:
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


@router.get("/stats")
async def get_system_stats(
    current_user: User = Depends(require_admin()),
    db: AsyncSession = Depends(get_db),
):
    """Get system-wide statistics"""
    from models.prompt import Prompt
    from models.ai_run import AIRun
    from models.organization import Organization

    user_count = await db.execute(select(func.count(User.id)))
    prompt_count = await db.execute(select(func.count(Prompt.id)))
    run_count = await db.execute(select(func.count(AIRun.id)))
    org_count = await db.execute(select(func.count(Organization.id)))
    total_cost = await db.execute(select(func.coalesce(func.sum(AIRun.cost_usd), 0)))
    total_tokens = await db.execute(select(func.coalesce(func.sum(AIRun.total_tokens), 0)))

    return {
        "total_users": user_count.scalar(),
        "total_prompts": prompt_count.scalar(),
        "total_ai_runs": run_count.scalar(),
        "total_organizations": org_count.scalar(),
        "total_cost_usd": float(total_cost.scalar()),
        "total_tokens": int(total_tokens.scalar()),
    }