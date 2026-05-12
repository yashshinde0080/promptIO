from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from dependencies import get_current_active_user
from models.user import User
from schemas.prompt import OptimizeRequest, EvaluateRequest, CompareRequest
from services.optimization_service import optimization_service
from services.evaluation_service import EvaluationService
from services.ai_router_service import ai_router_service
from services.audit_service import audit_service
from models.audit import AuditAction
from utils.helpers import get_client_ip
import json
import asyncio

router = APIRouter(prefix="/optimize", tags=["Optimization"])
evaluation_service_instance = EvaluationService()


@router.post("")
@router.post("/")
async def optimize_prompt(
    data: OptimizeRequest,
    request: Request,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Optimize a prompt using the specified framework.
    Core optimization endpoint - runs the full optimization pipeline.
    """
    try:
        result = await optimization_service.optimize(
            prompt=data.prompt,
            framework=data.framework.value,
            model=data.model,
            context=data.context,
            target_audience=data.target_audience,
            tone=data.tone,
            additional_instructions=data.additional_instructions,
            auto_detect_framework=data.auto_detect_framework or False,
            user_id=str(current_user.id),
            organization_id=str(current_user.organization_id) if current_user.organization_id else None,
        )

        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"],
            )

        # Save to DB if requested
        if data.save_result and result.get("optimized_prompt"):
            from services.prompt_service import prompt_service
            from schemas.prompt import PromptCreateRequest
            from models.prompt import PromptFramework

            create_req = PromptCreateRequest(
                title=data.title or f"Optimized: {data.prompt[:50]}...",
                original_content=data.prompt,
                framework=data.framework,
                framework_data=result.get("framework_data", {}),
            )
            prompt = await prompt_service.create_prompt(create_req, current_user, db)
            await prompt_service.save_optimized_result(
                str(prompt.id),
                result["optimized_prompt"],
                result.get("framework_data", {}),
                db,
            )
            result["prompt_id"] = str(prompt.id)

        await audit_service.log(
            db=db,
            action=AuditAction.PROMPT_OPTIMIZE,
            user_id=str(current_user.id),
            details={
                "framework": data.framework.value,
                "model": result.get("model_used"),
                "optimization_score": result.get("optimization_score"),
                "cost_usd": result.get("cost_usd"),
            },
            ip_address=get_client_ip(request),
        )

        return result

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Optimization failed: {str(e)}",
        )


@router.post("/stream")
async def stream_optimize(
    data: OptimizeRequest,
    current_user: User = Depends(get_current_active_user),
):
    """Stream optimization results in real-time"""

    from frameworks import get_framework
    framework_handler = get_framework(data.framework.value)
    messages = framework_handler.get_messages(original_prompt=data.prompt)
    selected_model = data.model or ai_router_service.default_model

    async def generate():
        try:
            yield f"data: {json.dumps({'type': 'start', 'model': selected_model})}\n\n"

            async for chunk in ai_router_service.stream_chat_completion(
                messages=messages,
                model=selected_model,
                temperature=0.4,
            ):
                yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"
                await asyncio.sleep(0)

            yield f"data: {json.dumps({'type': 'done'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/evaluate")
async def evaluate_prompt(
    data: EvaluateRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Evaluate prompt quality across multiple dimensions"""
    try:
        prompt_content = data.prompt_content
        
        if data.prompt_id and not prompt_content:
            from services.prompt_service import prompt_service
            prompt = await prompt_service.get_prompt(data.prompt_id, current_user, db)
            if not prompt:
                raise HTTPException(status_code=404, detail="Prompt not found")
            prompt_content = prompt.optimized_content or prompt.original_content

        if not prompt_content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either prompt_id or prompt_content is required",
            )

        from engines.evaluation_engine import evaluation_engine
        result = await evaluation_engine.evaluate_prompt(
            prompt_content=prompt_content,
            ai_router_service=ai_router_service if data.run_full_evaluation else None,
            model=data.model,
        )

        return {
            "prompt_id": data.prompt_id,
            "evaluation": result,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/compare")
async def compare_prompts(
    data: CompareRequest,
    current_user: User = Depends(get_current_active_user),
):
    """Compare two prompts side-by-side"""
    try:
        from engines.evaluation_engine import evaluation_engine

        result_a, result_b = await asyncio.gather(
            evaluation_engine.evaluate_prompt(
                prompt_content=data.prompt_a,
                ai_router_service=ai_router_service,
                model=data.model,
            ),
            evaluation_engine.evaluate_prompt(
                prompt_content=data.prompt_b,
                ai_router_service=ai_router_service,
                model=data.model,
            ),
        )

        score_a = result_a.get("overall_quality_score", 0)
        score_b = result_b.get("overall_quality_score", 0)

        return {
            "prompt_a": {
                "content": data.prompt_a,
                "evaluation": result_a,
            },
            "prompt_b": {
                "content": data.prompt_b,
                "evaluation": result_b,
            },
            "winner": "a" if score_a > score_b else "b" if score_b > score_a else "tie",
            "score_difference": abs(score_a - score_b),
            "recommendation": (
                "Prompt A is significantly better" if score_a - score_b > 0.2
                else "Prompt B is significantly better" if score_b - score_a > 0.2
                else "Prompts are comparable in quality"
            ),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/frameworks")
async def get_frameworks():
    """Get all available optimization frameworks"""
    frameworks = [
        {
            "id": "standard",
            "name": "Standard",
            "description": "General purpose optimized prompt generation",
            "use_cases": ["General queries", "Information requests", "Simple tasks"],
            "complexity": "low",
        },
        {
            "id": "reasoning",
            "name": "Reasoning",
            "description": "Multi-step reasoning and complex problem solving",
            "use_cases": ["Math problems", "Logic puzzles", "Complex analysis"],
            "complexity": "high",
        },
        {
            "id": "race",
            "name": "RACE",
            "description": "Role, Action, Context, Explanation",
            "use_cases": ["Expert consultations", "Professional advice", "Specialized tasks"],
            "complexity": "medium",
        },
        {
            "id": "care",
            "name": "CARE",
            "description": "Context, Action, Result, Example",
            "use_cases": ["Practical guidance", "How-to instructions", "Real-world scenarios"],
            "complexity": "medium",
        },
        {
            "id": "ape",
            "name": "APE",
            "description": "Action, Purpose, Execution",
            "use_cases": ["Task automation", "Goal-oriented work", "Process execution"],
            "complexity": "medium",
        },
        {
            "id": "create",
            "name": "CREATE",
            "description": "Character, Request, Examples, Adjustments, Type, Extras",
            "use_cases": ["Content creation", "Complex generation", "Guided outputs"],
            "complexity": "high",
        },
        {
            "id": "tag",
            "name": "TAG",
            "description": "Task, Action, Goal",
            "use_cases": ["Step-by-step tasks", "Workflow optimization", "Process design"],
            "complexity": "low",
        },
        {
            "id": "creo",
            "name": "CREO",
            "description": "Context, Request, Explanation, Outcome",
            "use_cases": ["Strategic planning", "Problem solving", "Idea generation"],
            "complexity": "medium",
        },
        {
            "id": "rise",
            "name": "RISE",
            "description": "Role, Input, Steps, Execution",
            "use_cases": ["Learning flows", "Training content", "Tutorial creation"],
            "complexity": "medium",
        },
        {
            "id": "pain",
            "name": "PAIN",
            "description": "Problem, Action, Information, Next Steps",
            "use_cases": ["Troubleshooting", "Problem resolution", "Debugging"],
            "complexity": "medium",
        },
        {
            "id": "coast",
            "name": "COAST",
            "description": "Context, Objective, Actions, Scenario, Task",
            "use_cases": ["Process planning", "Enterprise workflows", "Complex projects"],
            "complexity": "high",
        },
        {
            "id": "roses",
            "name": "ROSES",
            "description": "Role, Objective, Scenario, Expected Solution, Steps",
            "use_cases": ["Scenario analysis", "Decision making", "Case studies"],
            "complexity": "high",
        },
        {
            "id": "resee",
            "name": "RESEE",
            "description": "Role, Elaboration, Scenario, Elaboration, Examples",
            "use_cases": ["Deep role simulation", "Expert immersion", "Complex roleplay"],
            "complexity": "very_high",
        },
    ]
    return {"frameworks": frameworks, "total": len(frameworks)}


@router.get("/model")
async def get_current_model(
    current_user: User = Depends(get_current_active_user),
):
    """Get current configured AI model"""
    return ai_router_service.get_model_info()