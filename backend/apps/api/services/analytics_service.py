from typing import Dict, Any, Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from models.prompt import Prompt, PromptFramework
from models.ai_run import AIRun, AIRunStatus
from models.evaluation import Evaluation
from models.user import User
import structlog

logger = structlog.get_logger(__name__)


class AnalyticsService:

    async def get_dashboard_metrics(
        self,
        user: User,
        db: AsyncSession,
        days: int = 30,
    ) -> Dict[str, Any]:
        since = datetime.now(timezone.utc) - timedelta(days=days)
        org_filter = user.organization_id

        # Total prompts
        prompt_count = await db.execute(
            select(func.count(Prompt.id)).where(Prompt.owner_id == user.id)
        )
        total_prompts = prompt_count.scalar() or 0

        # AI Runs
        runs_result = await db.execute(
            select(
                func.count(AIRun.id),
                func.coalesce(func.sum(AIRun.total_tokens), 0),
                func.coalesce(func.sum(AIRun.cost_usd), 0),
                func.coalesce(func.avg(AIRun.latency_ms), 0),
            ).where(
                and_(
                    AIRun.user_id == user.id,
                    AIRun.created_at >= since,
                )
            )
        )
        runs_row = runs_result.one()
        total_runs = runs_row[0] or 0
        total_tokens = int(runs_row[1] or 0)
        total_cost = float(runs_row[2] or 0)
        avg_latency = float(runs_row[3] or 0)

        # Framework distribution
        framework_result = await db.execute(
            select(Prompt.framework, func.count(Prompt.id))
            .where(Prompt.owner_id == user.id)
            .group_by(Prompt.framework)
            .order_by(func.count(Prompt.id).desc())
        )
        framework_dist = [
            {"framework": str(row[0]), "count": row[1]}
            for row in framework_result
        ]

        # Daily runs over time (last N days)
        daily_runs = await self._get_daily_runs(user, db, days)

        # Average quality score
        quality_result = await db.execute(
            select(func.avg(Evaluation.overall_quality_score)).where(
                Evaluation.prompt_id.in_(
                    select(Prompt.id).where(Prompt.owner_id == user.id)
                )
            )
        )
        avg_quality = float(quality_result.scalar() or 0)

        return {
            "period_days": days,
            "total_prompts": total_prompts,
            "total_runs": total_runs,
            "total_tokens": total_tokens,
            "total_cost_usd": round(total_cost, 4),
            "avg_latency_ms": round(avg_latency, 2),
            "avg_quality_score": round(avg_quality, 3),
            "framework_distribution": framework_dist,
            "daily_runs": daily_runs,
            "success_rate": await self._get_success_rate(user, db, since),
        }

    async def _get_daily_runs(
        self, user: User, db: AsyncSession, days: int
    ) -> list:
        since = datetime.now(timezone.utc) - timedelta(days=days)
        day_col = func.date_trunc("day", AIRun.created_at).label("day")
        result = await db.execute(
            select(
                day_col,
                func.count(AIRun.id).label("count"),
                func.coalesce(func.sum(AIRun.cost_usd), 0).label("cost"),
            )
            .where(
                and_(
                    AIRun.user_id == user.id,
                    AIRun.created_at >= since,
                )
            )
            .group_by(day_col)
            .order_by(day_col)
        )
        return [
            {
                "date": str(row.day)[:10] if row.day else None,
                "runs": row.count,
                "cost": float(row.cost),
            }
            for row in result
        ]

    async def _get_success_rate(
        self, user: User, db: AsyncSession, since: datetime
    ) -> float:
        total_result = await db.execute(
            select(func.count(AIRun.id)).where(
                and_(AIRun.user_id == user.id, AIRun.created_at >= since)
            )
        )
        total = total_result.scalar() or 0
        if total == 0:
            return 1.0

        success_result = await db.execute(
            select(func.count(AIRun.id)).where(
                and_(
                    AIRun.user_id == user.id,
                    AIRun.created_at >= since,
                    AIRun.status == AIRunStatus.COMPLETED,
                )
            )
        )
        success = success_result.scalar() or 0
        return round(success / total, 3)


analytics_service = AnalyticsService()