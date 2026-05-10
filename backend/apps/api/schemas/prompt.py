from pydantic import BaseModel, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from models.prompt import PromptFramework, PromptVisibility, PromptStatus


class PromptCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    original_content: str
    framework: PromptFramework
    framework_data: Optional[Dict[str, Any]] = {}
    variables: Optional[List[str]] = []
    tags: Optional[List[str]] = []
    visibility: Optional[PromptVisibility] = PromptVisibility.PRIVATE
    is_template: Optional[bool] = False

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if len(v.strip()) < 3:
            raise ValueError("Title must be at least 3 characters")
        if len(v) > 500:
            raise ValueError("Title must not exceed 500 characters")
        return v.strip()

    @field_validator("original_content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        if len(v.strip()) < 10:
            raise ValueError("Prompt content must be at least 10 characters")
        if len(v) > 50000:
            raise ValueError("Prompt content must not exceed 50000 characters")
        return v.strip()


class PromptUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    original_content: Optional[str] = None
    framework: Optional[PromptFramework] = None
    framework_data: Optional[Dict[str, Any]] = None
    variables: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    visibility: Optional[PromptVisibility] = None
    status: Optional[PromptStatus] = None
    is_pinned: Optional[bool] = None
    change_summary: Optional[str] = None


class OptimizeRequest(BaseModel):
    prompt: str
    framework: PromptFramework
    model: Optional[str] = None
    context: Optional[str] = None
    target_audience: Optional[str] = None
    tone: Optional[str] = None
    additional_instructions: Optional[str] = None
    auto_detect_framework: Optional[bool] = False
    save_result: Optional[bool] = False
    title: Optional[str] = None

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, v: str) -> str:
        if len(v.strip()) < 5:
            raise ValueError("Prompt must be at least 5 characters")
        return v.strip()


class EvaluateRequest(BaseModel):
    prompt_id: Optional[str] = None
    prompt_content: Optional[str] = None
    model: Optional[str] = None
    run_full_evaluation: Optional[bool] = True


class CompareRequest(BaseModel):
    prompt_a: str
    prompt_b: str
    model: Optional[str] = None
    evaluation_criteria: Optional[List[str]] = None


class PromptResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    original_content: str
    optimized_content: Optional[str]
    framework: str
    framework_data: Dict[str, Any]
    variables: List[str]
    tags: List[str]
    status: str
    visibility: str
    version: int
    is_template: bool
    is_pinned: bool
    owner_id: str
    organization_id: Optional[str]
    total_runs: int
    avg_quality_score: float
    avg_latency_ms: float
    total_tokens_used: int
    total_cost_usd: float
    pii_detected: bool
    safety_score: float
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class OptimizeResponse(BaseModel):
    original_prompt: str
    optimized_prompt: str
    framework: str
    framework_data: Dict[str, Any]
    improvements: List[str]
    token_count_before: int
    token_count_after: int
    optimization_score: float
    model_used: str
    latency_ms: float
    prompt_id: Optional[str] = None


class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    per_page: int
    pages: int