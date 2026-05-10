from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from database import get_db
from dependencies import get_current_active_user
from models.user import User
from schemas.prompt import (
    PromptCreateRequest, PromptUpdateRequest,
    PromptResponse, PaginatedResponse
)
from services.prompt_service import prompt_service
from services.audit_service import audit_service
from models.audit import AuditAction
from utils.helpers import paginate

router = APIRouter(prefix="/prompts", tags=["Prompts"])


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_prompt(
    data: PromptCreateRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new prompt"""
    try:
        prompt = await prompt_service.create_prompt(data, current_user, db)
        
        await audit_service.log(
            db=db,
            action=AuditAction.PROMPT_CREATE,
            user_id=str(current_user.id),
            resource_type="prompt",
            resource_id=str(prompt.id),
            details={"title": prompt.title, "framework": str(prompt.framework)},
        )

        return {
            "id": str(prompt.id),
            "title": prompt.title,
            "framework": str(prompt.framework),
            "status": str(prompt.status),
            "message": "Prompt created successfully",
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/")
async def list_prompts(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    framework: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
    search: Optional[str] = Query(default=None),
    visibility: Optional[str] = Query(default=None),
    is_template: Optional[bool] = Query(default=None),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """List prompts with filtering and pagination"""
    prompts, total = await prompt_service.list_prompts(
        user=current_user,
        db=db,
        page=page,
        per_page=per_page,
        framework=framework,
        status=status,
        search=search,
        visibility=visibility,
        is_template=is_template,
    )

    prompt_list = []
    for p in prompts:
        prompt_list.append({
            "id": str(p.id),
            "title": p.title,
            "description": p.description,
            "framework": str(p.framework),
            "status": str(p.status),
            "visibility": str(p.visibility),
            "version": p.version,
            "is_template": p.is_template,
            "is_pinned": p.is_pinned,
            "tags": p.tags or [],
            "total_runs": p.total_runs,
            "avg_quality_score": p.avg_quality_score,
            "total_cost_usd": p.total_cost_usd,
            "created_at": str(p.created_at),
            "updated_at": str(p.updated_at) if p.updated_at else None,
        })

    return {
        "items": prompt_list,
        **paginate(total, page, per_page),
    }


@router.get("/{prompt_id}")
async def get_prompt(
    prompt_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific prompt by ID"""
    try:
        prompt = await prompt_service.get_prompt(prompt_id, current_user, db)
        if not prompt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Prompt not found",
            )

        return {
            "id": str(prompt.id),
            "title": prompt.title,
            "description": prompt.description,
            "original_content": prompt.original_content,
            "optimized_content": prompt.optimized_content,
            "framework": str(prompt.framework),
            "framework_data": prompt.framework_data,
            "variables": prompt.variables,
            "tags": prompt.tags,
            "status": str(prompt.status),
            "visibility": str(prompt.visibility),
            "version": prompt.version,
            "is_template": prompt.is_template,
            "is_pinned": prompt.is_pinned,
            "owner_id": str(prompt.owner_id),
            "organization_id": str(prompt.organization_id) if prompt.organization_id else None,
            "total_runs": prompt.total_runs,
            "avg_quality_score": prompt.avg_quality_score,
            "avg_latency_ms": prompt.avg_latency_ms,
            "total_tokens_used": prompt.total_tokens_used,
            "total_cost_usd": prompt.total_cost_usd,
            "pii_detected": prompt.pii_detected,
            "safety_score": prompt.safety_score,
            "compliance_flags": prompt.compliance_flags,
            "created_at": str(prompt.created_at),
            "updated_at": str(prompt.updated_at) if prompt.updated_at else None,
        }
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.put("/{prompt_id}")
async def update_prompt(
    prompt_id: str,
    data: PromptUpdateRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Update an existing prompt"""
    try:
        prompt = await prompt_service.update_prompt(prompt_id, data, current_user, db)

        await audit_service.log(
            db=db,
            action=AuditAction.PROMPT_UPDATE,
            user_id=str(current_user.id),
            resource_type="prompt",
            resource_id=prompt_id,
            details={"version": prompt.version},
        )

        return {
            "id": str(prompt.id),
            "title": prompt.title,
            "version": prompt.version,
            "message": "Prompt updated successfully",
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.delete("/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prompt(
    prompt_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a prompt"""
    try:
        await prompt_service.delete_prompt(prompt_id, current_user, db)
        await audit_service.log(
            db=db,
            action=AuditAction.PROMPT_DELETE,
            user_id=str(current_user.id),
            resource_type="prompt",
            resource_id=prompt_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.get("/{prompt_id}/versions")
async def get_versions(
    prompt_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get version history of a prompt"""
    try:
        versions = await prompt_service.get_versions(prompt_id, current_user, db)
        return {
            "prompt_id": prompt_id,
            "versions": [
                {
                    "id": str(v.id),
                    "version": v.version,
                    "content": v.content,
                    "optimized_content": v.optimized_content,
                    "change_summary": v.change_summary,
                    "change_type": v.change_type,
                    "created_by": str(v.created_by),
                    "created_at": str(v.created_at),
                }
                for v in versions
            ],
            "total": len(versions),
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))