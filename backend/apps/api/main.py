import structlog
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from config import settings
from database import init_db, close_db
from middleware.logging_middleware import LoggingMiddleware
from middleware.rate_limit import RateLimitMiddleware
from routers import auth, prompts, optimize, analytics, admin, audit, health


# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer() if not settings.DEBUG
        else structlog.dev.ConsoleRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logging.basicConfig(level=logging.DEBUG if settings.DEBUG else logging.INFO)
logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(
        "Starting PromptIO API",
        environment=settings.APP_ENV,
        debug=settings.DEBUG,
    )
    await init_db()
    logger.info("PromptIO API started successfully")
    yield
    logger.info("Shutting down PromptIO API")
    await close_db()
    logger.info("PromptIO API shutdown complete")


app = FastAPI(
    title="PromptIO API",
    description="""
    # PromptIO - Intelligent Prompt Optimizer Platform
    
    Enterprise-grade AI prompt engineering platform with 13 optimization frameworks,
    multi-model support via OpenRouter, evaluation engine, and compliance features.
    
    ## Features
    - 13 Prompt Frameworks (RACE, CARE, APE, CREATE, TAG, CREO, RISE, PAIN, COAST, ROSES, RESEE, Standard, Reasoning)
    - Multi-model AI routing (GPT-4o, Claude, Gemini, Llama, Mistral, DeepSeek)
    - Prompt evaluation and scoring
    - Version control for prompts
    - Enterprise RBAC
    - GDPR compliance
    - Audit logging
    - Real-time streaming
    """,
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# -------------------------------------------------------
# Middleware Stack (Order matters - outermost first)
# -------------------------------------------------------

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time", "X-RateLimit-Remaining"],
)

# GZip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Rate limiting
app.add_middleware(RateLimitMiddleware)

# Request logging
app.add_middleware(LoggingMiddleware)


# -------------------------------------------------------
# Exception Handlers
# -------------------------------------------------------

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })

    logger.warning(
        "Validation error",
        path=str(request.url),
        errors=errors,
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "message": "Request validation failed",
            "details": errors,
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        "Unhandled exception",
        path=str(request.url),
        method=request.method,
        error=str(exc),
        exc_info=True,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later.",
            "request_id": getattr(request.state, "request_id", "unknown"),
        },
    )


# -------------------------------------------------------
# Routers
# -------------------------------------------------------

app.include_router(health.router)
app.include_router(auth.router, prefix="/api/v1")
app.include_router(prompts.router, prefix="/api/v1")
app.include_router(optimize.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
app.include_router(audit.router, prefix="/api/v1")


# -------------------------------------------------------
# Root
# -------------------------------------------------------

@app.get("/", tags=["Root"])
async def root():
    return {
        "service": "PromptIO API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs" if settings.DEBUG else "Contact admin for API documentation",
        "frameworks": [
            "standard", "reasoning", "race", "care", "ape",
            "create", "tag", "creo", "rise", "pain", "coast", "roses", "resee"
        ],
    }


@app.get("/api/v1", tags=["Root"])
async def api_root():
    return {
        "api_version": "v1",
        "endpoints": {
            "auth": "/api/v1/auth",
            "prompts": "/api/v1/prompts",
            "optimize": "/api/v1/optimize",
            "analytics": "/api/v1/analytics",
            "admin": "/api/v1/admin",
            "health": "/api/v1/health",
            "docs": "/docs" if settings.DEBUG else "Contact admin for API documentation",
            "frameworks": [
                "standard", "reasoning", "race", "care", "ape",
                "create", "tag", "creo", "rise", "pain", "coast", "roses", "resee",
            ],
        },
    }