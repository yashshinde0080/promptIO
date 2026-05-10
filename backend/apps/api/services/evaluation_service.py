from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from models.evaluation import Evaluation, EvaluationStatus
from engines.evaluation_engine import evaluation_engine
from services.ai_router_service import ai_router_service
from datetime import datetime, timezone
import structlog

logger = structlog.get_logger(__name__)


class EvaluationService:

    async def run_evaluation(
        self,
        prompt_content: str,
        prompt_id: Optional[str] = None,
        model: Optional[str] = None,
        db: Optional[AsyncSession] = None,
        run_full: bool = True,
    ) -> Dict[str, Any]:
        
        ai_service = ai_router_service if run_full else None
        
        result = await evaluation_engine.evaluate_prompt(
            prompt_content=prompt_content,
            ai_router_service=ai_service,
            model=model,
        )

        if db and prompt_id:
            evaluation = Evaluation(
                prompt_id=prompt_id,
                status=EvaluationStatus.COMPLETED,
                model_used=model,
                relevance_score=result.get("relevance_score"),
                accuracy_score=result.get("clarity_score"),
                clarity_score=result.get("clarity_score"),
                specificity_score=result.get("specificity_score"),
                safety_score=result.get("safety_score"),
                reasoning_depth_score=result.get("reasoning_depth_score"),
                overall_quality_score=result.get("overall_quality_score"),
                latency_ms=result.get("latency_ms"),
                hallucination_risk=result.get("hallucination_risk"),
                ambiguity_score=result.get("ambiguity_score"),
                complexity_score=result.get("complexity_score"),
                strengths=result.get("strengths", []),
                weaknesses=result.get("weaknesses", []),
                suggestions=result.get("suggestions", []),
                detailed_feedback=result.get("detailed_feedback"),
                pii_detected=result.get("pii_detected", []),
                compliance_issues=result.get("compliance_issues", []),
                completed_at=datetime.now(timezone.utc),
            )
            db.add(evaluation)

        return result