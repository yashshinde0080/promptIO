import time
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import structlog

logger = structlog.get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())[:8]
        start_time = time.time()

        # Add request ID to request state
        request.state.request_id = request_id

        logger.info(
            "Request started",
            request_id=request_id,
            method=request.method,
            url=str(request.url),
            client_ip=request.client.host if request.client else "unknown",
        )

        try:
            response = await call_next(request)
            process_time = (time.time() - start_time) * 1000

            logger.info(
                "Request completed",
                request_id=request_id,
                method=request.method,
                url=str(request.url),
                status_code=response.status_code,
                latency_ms=round(process_time, 2),
            )

            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(round(process_time, 2))
            return response

        except Exception as e:
            process_time = (time.time() - start_time) * 1000
            logger.error(
                "Request failed",
                request_id=request_id,
                method=request.method,
                url=str(request.url),
                error=str(e),
                latency_ms=round(process_time, 2),
            )
            raise