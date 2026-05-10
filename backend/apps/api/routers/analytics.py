from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from dependencies import get_current_active_user
from models.user import User
from services.analytics_service import analytics_service

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard")
async def get_dashboard_metrics(
    days: int = Query(default=30, ge=1, le=365),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get comprehensive dashboard metrics"""
    metrics = await analytics_service.get_dashboard_metrics(current_user, db, days)
    return metrics


@router.get("/cost")
async def get_cost_analytics(
    days: int = Query(default=30, ge=1, le=365),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get cost breakdown analytics"""
    from sqlalchemy import select, func, and_
    from datetime import datetime, timedelta, timezone
    from models.ai_run import AIRun

    since = datetime.now(timezone.utc) - timedelta(days=days)

    result = await db.execute(
        select(
            AIRun.model,
            func.count(AIRun.id).label("runs"),
            func.coalesce(func.sum(AIRun.cost_usd), 0).label("total_cost"),
            func.coalesce(func.sum(AIRun.total_tokens), 0).label("total_tokens"),
        )
        .where(and_(AIRun.user_id == current_user.id, AIRun.created_at >= since))
        .group_by(AIRun.model)
        .order_by(func.sum(AIRun.cost_usd).desc())
    )

    by_model = [
        {
            "model": row.model,
            "runs": row.runs,
            "total_cost": float(row.total_cost),
            "total_tokens": int(row.total_tokens),
            "avg_cost_per_run": float(row.total_cost) / row.runs if row.runs > 0 else 0,
        }
        for row in result
    ]

    return {
        "period_days": days,
        "by_model": by_model,
        "total_cost": sum(m["total_cost"] for m in by_model),
    }


@router.get("/usage")
async def get_usage_analytics(
    days: int = Query(default=30, ge=1, le=365),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get token usage analytics"""
    metrics = await analytics_service.get_dashboard_metrics(current_user, db, days)
    return {
        "period_days": days,
        "total_tokens": metrics["total_tokens"],
        "total_runs": metrics["total_runs"],
        "avg_tokens_per_run": (
            metrics["total_tokens"] / metrics["total_runs"]
            if metrics["total_runs"] > 0 else 0
        ),
        "daily_usage": metrics["daily_runs"],
        "framework_distribution": metrics["framework_distribution"],
    }


@router.get("/performance")
async def get_performance_analytics(
    days: int = Query(default=30, ge=1, le=365),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get performance analytics"""
    metrics = await analytics_service.get_dashboard_metrics(current_user, db, days)
    return {
        "period_days": days,
        "avg_latency_ms": metrics["avg_latency_ms"],
        "avg_quality_score": metrics["avg_quality_score"],
        "success_rate": metrics["success_rate"],
        "total_runs": metrics["total_runs"],
        "daily_trends": metrics["daily_runs"],
    }