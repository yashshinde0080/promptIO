import httpx
import time
import json
import asyncio
from typing import Dict, Any, List, Optional, AsyncGenerator
from config import settings
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential

logger = structlog.get_logger(__name__)


AVAILABLE_MODELS = {
    "openai/gpt-4o": {
        "name": "GPT-4o",
        "provider": "OpenAI",
        "context_window": 128000,
        "cost_per_1k_input": 0.005,
        "cost_per_1k_output": 0.015,
        "best_for": ["general", "reasoning", "code"],
        "tier": "premium",
    },
    "openai/gpt-4o-mini": {
        "name": "GPT-4o Mini",
        "provider": "OpenAI",
        "context_window": 128000,
        "cost_per_1k_input": 0.00015,
        "cost_per_1k_output": 0.0006,
        "best_for": ["fast", "cheap", "simple"],
        "tier": "economy",
    },
    "anthropic/claude-3.5-sonnet": {
        "name": "Claude 3.5 Sonnet",
        "provider": "Anthropic",
        "context_window": 200000,
        "cost_per_1k_input": 0.003,
        "cost_per_1k_output": 0.015,
        "best_for": ["analysis", "writing", "complex"],
        "tier": "premium",
    },
    "anthropic/claude-3-haiku": {
        "name": "Claude 3 Haiku",
        "provider": "Anthropic",
        "context_window": 200000,
        "cost_per_1k_input": 0.00025,
        "cost_per_1k_output": 0.00125,
        "best_for": ["fast", "economy", "simple"],
        "tier": "economy",
    },
    "google/gemini-pro-1.5": {
        "name": "Gemini Pro 1.5",
        "provider": "Google",
        "context_window": 1000000,
        "cost_per_1k_input": 0.00125,
        "cost_per_1k_output": 0.005,
        "best_for": ["long_context", "multimodal"],
        "tier": "standard",
    },
    "meta-llama/llama-3.1-70b-instruct": {
        "name": "Llama 3.1 70B",
        "provider": "Meta",
        "context_window": 131072,
        "cost_per_1k_input": 0.00052,
        "cost_per_1k_output": 0.00075,
        "best_for": ["open_source", "reasoning"],
        "tier": "standard",
    },
    "mistralai/mistral-large": {
        "name": "Mistral Large",
        "provider": "Mistral AI",
        "context_window": 32000,
        "cost_per_1k_input": 0.004,
        "cost_per_1k_output": 0.012,
        "best_for": ["multilingual", "reasoning"],
        "tier": "standard",
    },
    "deepseek/deepseek-chat": {
        "name": "DeepSeek Chat",
        "provider": "DeepSeek",
        "context_window": 65536,
        "cost_per_1k_input": 0.00014,
        "cost_per_1k_output": 0.00028,
        "best_for": ["economy", "code", "reasoning"],
        "tier": "economy",
    },
}


class AIRouterService:
    """
    Intelligent AI routing service using OpenRouter
    Handles model selection, streaming, retry logic, cost tracking
    """

    def __init__(self):
        self.base_url = settings.OPENROUTER_BASE_URL
        self.api_key = settings.OPENROUTER_API_KEY
        self.default_model = settings.OPENROUTER_DEFAULT_MODEL
        self.timeout = httpx.Timeout(120.0, connect=10.0)

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": settings.OPENROUTER_SITE_URL,
            "X-Title": settings.OPENROUTER_SITE_NAME,
        }

    def select_model(
        self,
        framework: str = "standard",
        preference: str = "balanced",
        allowed_models: Optional[List[str]] = None,
    ) -> str:
        """Intelligently select model based on framework and preference"""
        
        framework_model_map = {
            "reasoning": "anthropic/claude-3.5-sonnet",
            "roses": "anthropic/claude-3.5-sonnet",
            "resee": "anthropic/claude-3.5-sonnet",
            "coast": "openai/gpt-4o",
            "create": "openai/gpt-4o",
            "standard": "openai/gpt-4o-mini",
            "tag": "openai/gpt-4o-mini",
            "pain": "openai/gpt-4o-mini",
        }

        preference_map = {
            "cheapest": "deepseek/deepseek-chat",
            "fastest": "openai/gpt-4o-mini",
            "smartest": "anthropic/claude-3.5-sonnet",
            "balanced": framework_model_map.get(framework, self.default_model),
        }

        selected = preference_map.get(preference, self.default_model)

        if allowed_models and selected not in allowed_models:
            for model in allowed_models:
                if model in AVAILABLE_MODELS:
                    return model
            return self.default_model

        return selected

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format: Optional[Dict] = None,
        stream: bool = False,
    ) -> Dict[str, Any]:
        """Execute chat completion with retry logic"""

        selected_model = model or self.default_model
        start_time = time.time()

        payload = {
            "model": selected_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if response_format:
            payload["response_format"] = response_format

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self._get_headers(),
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()

                latency_ms = (time.time() - start_time) * 1000
                usage = data.get("usage", {})
                model_info = AVAILABLE_MODELS.get(selected_model, {})

                input_tokens = usage.get("prompt_tokens", 0)
                output_tokens = usage.get("completion_tokens", 0)
                cost_usd = (
                    input_tokens / 1000 * model_info.get("cost_per_1k_input", 0)
                    + output_tokens / 1000 * model_info.get("cost_per_1k_output", 0)
                )

                logger.info(
                    "AI completion successful",
                    model=selected_model,
                    latency_ms=round(latency_ms, 2),
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    cost_usd=round(cost_usd, 6),
                )

                return {
                    "content": data["choices"][0]["message"]["content"],
                    "model": selected_model,
                    "latency_ms": latency_ms,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": input_tokens + output_tokens,
                    "cost_usd": cost_usd,
                    "finish_reason": data["choices"][0].get("finish_reason", "stop"),
                }

            except httpx.HTTPStatusError as e:
                logger.error(
                    "OpenRouter API error",
                    status_code=e.response.status_code,
                    error=str(e),
                    model=selected_model,
                )
                raise
            except httpx.TimeoutException:
                logger.error("OpenRouter API timeout", model=selected_model)
                raise

    async def stream_chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> AsyncGenerator[str, None]:
        """Stream chat completion responses"""

        selected_model = model or self.default_model
        payload = {
            "model": selected_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            async with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                headers=self._get_headers(),
                json=payload,
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:]
                        if data_str.strip() == "[DONE]":
                            break
                        try:
                            data = json.loads(data_str)
                            delta = data["choices"][0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                yield content
                        except (json.JSONDecodeError, KeyError, IndexError):
                            continue

    def get_available_models(self) -> Dict[str, Any]:
        return AVAILABLE_MODELS

    def estimate_cost(
        self, model: str, input_tokens: int, output_tokens: int
    ) -> float:
        model_info = AVAILABLE_MODELS.get(model, {})
        return (
            input_tokens / 1000 * model_info.get("cost_per_1k_input", 0)
            + output_tokens / 1000 * model_info.get("cost_per_1k_output", 0)
        )


ai_router_service = AIRouterService()