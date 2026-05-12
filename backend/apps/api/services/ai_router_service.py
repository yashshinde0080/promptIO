import httpx
import time
import json
import asyncio
from typing import Dict, Any, List, Optional, AsyncGenerator
from config import settings
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception


def is_retriable(exc: BaseException) -> bool:
    if isinstance(exc, httpx.HTTPStatusError):
        if exc.response.status_code < 500:
            return False
    return True


logger = structlog.get_logger(__name__)


class AIRouterService:
    """
    AI routing service using OpenRouter.
    Uses a single model from env config (OPENROUTER_DEFAULT_MODEL).
    Handles streaming, retry logic, and cost tracking.
    """

    def __init__(self):
        self.base_url = settings.OPENROUTER_BASE_URL
        self.api_key = settings.OPENROUTER_API_KEY
        self.default_model = settings.OPENROUTER_DEFAULT_MODEL
        if self.default_model == "google/gemini-2.0-flash:free":
            self.default_model = "google/gemini-2.0-flash-lite-preview-02-05:free"
        self.timeout = httpx.Timeout(120.0, connect=10.0)

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": settings.OPENROUTER_SITE_URL,
            "X-Title": settings.OPENROUTER_SITE_NAME,
        }

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception(is_retriable),
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
        if selected_model == "google/gemini-2.0-flash:free":
            selected_model = "google/gemini-2.0-flash-lite-preview-02-05:free"
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

                input_tokens = usage.get("prompt_tokens", 0)
                output_tokens = usage.get("completion_tokens", 0)

                logger.info(
                    "AI completion successful",
                    model=selected_model,
                    latency_ms=round(latency_ms, 2),
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                )

                return {
                    "content": data["choices"][0]["message"]["content"],
                    "model": selected_model,
                    "latency_ms": latency_ms,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": input_tokens + output_tokens,
                    "cost_usd": 0,
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
        if selected_model == "google/gemini-2.0-flash:free":
            selected_model = "google/gemini-2.0-flash-lite-preview-02-05:free"
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

    def get_model_info(self) -> Dict[str, str]:
        """Return current model info"""
        return {
            "model": self.default_model,
            "base_url": self.base_url,
        }


ai_router_service = AIRouterService()