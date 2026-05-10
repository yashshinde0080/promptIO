import time
from collections import defaultdict
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from config import settings
import structlog

logger = structlog.get_logger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    In-memory rate limiter (use Redis for production)
    """

    def __init__(self, app, calls_per_minute: int = None):
        super().__init__(app)
        self.calls_per_minute = calls_per_minute or settings.RATE_LIMIT_PER_MINUTE
        self.requests = defaultdict(list)
        
        # Exempt paths
        self.exempt_paths = {"/health", "/docs", "/redoc", "/openapi.json"}

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.exempt_paths:
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        window_start = now - 60

        # Clean old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if req_time > window_start
        ]

        if len(self.requests[client_ip]) >= self.calls_per_minute:
            logger.warning(
                "Rate limit exceeded",
                client_ip=client_ip,
                path=request.url.path,
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "Rate limit exceeded",
                    "limit": self.calls_per_minute,
                    "window": "60 seconds",
                    "retry_after": 60,
                },
            )

        self.requests[client_ip].append(now)
        response = await call_next(request)
        
        remaining = self.calls_per_minute - len(self.requests[client_ip])
        response.headers["X-RateLimit-Limit"] = str(self.calls_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(max(0, remaining))
        response.headers["X-RateLimit-Reset"] = str(int(window_start + 60))
        
        return response