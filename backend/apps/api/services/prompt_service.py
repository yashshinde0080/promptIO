import uuid
from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func, desc, and_, or_
from sqlalchemy.orm import selectinload
from models.prompt import Prompt, PromptVersion, PromptFramework, PromptStatus, PromptVisibility
from models.user import User
from schemas.prompt import PromptCreateRequest, PromptUpdateRequest
from datetime import datetime, timezone
import structlog

logger = structlog.get_logger(__name__)


class PromptService:
    
    async def create_prompt(
        self,
        data: PromptCreateRequest,
        user: User,
        db: AsyncSession,
    ) -> Prompt:
        prompt = Prompt(
            title=data.title,
            description=data.description,
            original_content=data.original_content,
            framework=data.framework,
            framework_data=data.framework_data or {},
            variables=data.variables or [],
            tags=data.tags or [],
            visibility=data.visibility or PromptVisibility.PRIVATE,
            is_template=data.is_template or False,
            owner_id=user.id,
            organization_id=user.organization_id,
            status=PromptStatus.DRAFT,
            version=1,
        )

        db.add(prompt)
        await db.flush()

        # Create initial version
        version = PromptVersion(
            prompt_id=prompt.id,
            version=1,
            content=data.original_content,
            optimized_content=None,
            framework_data=data.framework_data or {},
            change_summary="Initial creation",
            change_type="create",
            created_by=user.id,
        )
        db.add(version)

        logger.info("Prompt created", prompt_id=str(prompt.id), user_id=str(user.id))
        return prompt

    async def get_prompt(
        self, prompt_id: str, user: User, db: AsyncSession
    ) -> Optional[Prompt]:
        result = await db.execute(
            select(Prompt)
            .where(Prompt.id == prompt_id)
            .options(selectinload(Prompt.owner))
        )
        prompt = result.scalar_one_or_none()

        if not prompt:
            return None

        if not self._can_access(prompt, user):
            raise PermissionError("Access denied to this prompt")

        return prompt

    async def list_prompts(
        self,
        user: User,
        db: AsyncSession,
        page: int = 1,
        per_page: int = 20,
        framework: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
        tags: Optional[List[str]] = None,
        visibility: Optional[str] = None,
        is_template: Optional[bool] = None,
    ) -> Tuple[List[Prompt], int]:
        
        query = select(Prompt).where(
            or_(
                Prompt.owner_id == user.id,
                and_(
                    Prompt.visibility == PromptVisibility.ORGANIZATION,
                    Prompt.organization_id == user.organization_id,
                ),
                Prompt.visibility == PromptVisibility.PUBLIC,
            )
        )

        if framework:
            query = query.where(Prompt.framework == framework)
        if status:
            query = query.where(Prompt.status == status)
        if visibility:
            query = query.where(Prompt.visibility == visibility)
        if is_template is not None:
            query = query.where(Prompt.is_template == is_template)
        if search:
            query = query.where(
                or_(
                    Prompt.title.ilike(f"%{search}%"),
                    Prompt.description.ilike(f"%{search}%"),
                )
            )
        if tags:
            for tag in tags:
                query = query.where(Prompt.tags.contains([tag]))

        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()

        query = (
            query
            .order_by(desc(Prompt.is_pinned), desc(Prompt.updated_at))
            .offset((page - 1) * per_page)
            .limit(per_page)
        )
        result = await db.execute(query)
        prompts = result.scalars().all()

        return list(prompts), total

    async def update_prompt(
        self,
        prompt_id: str,
        data: PromptUpdateRequest,
        user: User,
        db: AsyncSession,
    ) -> Prompt:
        prompt = await self.get_prompt(prompt_id, user, db)
        if not prompt:
            raise ValueError("Prompt not found")
        if str(prompt.owner_id) != str(user.id):
            raise PermissionError("Only the owner can update this prompt")

        old_content = prompt.original_content
        update_data = data.model_dump(exclude_none=True, exclude={"change_summary"})

        for key, value in update_data.items():
            setattr(prompt, key, value)

        # Create new version if content changed
        if data.original_content and data.original_content != old_content:
            prompt.version += 1
            version = PromptVersion(
                prompt_id=prompt.id,
                version=prompt.version,
                content=data.original_content,
                optimized_content=prompt.optimized_content,
                framework_data=prompt.framework_data,
                change_summary=data.change_summary or "Content updated",
                change_type="update",
                created_by=user.id,
            )
            db.add(version)

        logger.info("Prompt updated", prompt_id=prompt_id, user_id=str(user.id))
        return prompt

    async def delete_prompt(
        self, prompt_id: str, user: User, db: AsyncSession
    ) -> bool:
        prompt = await self.get_prompt(prompt_id, user, db)
        if not prompt:
            raise ValueError("Prompt not found")
        if str(prompt.owner_id) != str(user.id):
            raise PermissionError("Only the owner can delete this prompt")

        await db.execute(delete(Prompt).where(Prompt.id == prompt_id))
        logger.info("Prompt deleted", prompt_id=prompt_id, user_id=str(user.id))
        return True

    async def save_optimized_result(
        self,
        prompt_id: str,
        optimized_content: str,
        framework_data: Dict[str, Any],
        db: AsyncSession,
    ) -> None:
        await db.execute(
            update(Prompt)
            .where(Prompt.id == prompt_id)
            .values(
                optimized_content=optimized_content,
                framework_data=framework_data,
                updated_at=datetime.now(timezone.utc),
            )
        )

    async def get_versions(
        self, prompt_id: str, user: User, db: AsyncSession
    ) -> List[PromptVersion]:
        prompt = await self.get_prompt(prompt_id, user, db)
        if not prompt:
            raise ValueError("Prompt not found")

        result = await db.execute(
            select(PromptVersion)
            .where(PromptVersion.prompt_id == prompt_id)
            .order_by(desc(PromptVersion.version))
        )
        return list(result.scalars().all())

    async def get_analytics(
        self, user: User, db: AsyncSession
    ) -> Dict[str, Any]:
        total_result = await db.execute(
            select(func.count(Prompt.id)).where(Prompt.owner_id == user.id)
        )
        total_prompts = total_result.scalar()

        framework_result = await db.execute(
            select(Prompt.framework, func.count(Prompt.id))
            .where(Prompt.owner_id == user.id)
            .group_by(Prompt.framework)
        )
        by_framework = {str(row[0]): row[1] for row in framework_result}

        return {
            "total_prompts": total_prompts,
            "by_framework": by_framework,
            "total_runs": 0,
            "avg_quality_score": 0.0,
        }

    def _can_access(self, prompt: Prompt, user: User) -> bool:
        if str(prompt.owner_id) == str(user.id):
            return True
        if prompt.visibility == PromptVisibility.PUBLIC:
            return True
        if (
            prompt.visibility == PromptVisibility.ORGANIZATION
            and prompt.organization_id
            and str(prompt.organization_id) == str(user.organization_id)
        ):
            return True
        return False


prompt_service = PromptService()