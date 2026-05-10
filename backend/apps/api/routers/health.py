from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db
from config import settings
import time

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": "1.0.0",
        "environment": settings.APP_ENV,
        "timestamp": time.time(),
    }


@router.get("/health/detailed")
async def detailed_health_check(db: AsyncSession = Depends(get_db)):
    """Detailed health check with DB connectivity"""
    health = {
        "status": "healthy",
        "service": settings.APP_NAME,
        "timestamp": time.time(),
        "checks": {},
    }

    # Database check
    try:
        await db.execute(text("SELECT 1"))
        health["checks"]["database"] = {"status": "healthy", "latency_ms": 0}
    except Exception as e:
        health["checks"]["database"] = {"status": "unhealthy", "error": str(e)}
        health["status"] = "degraded"

    # OpenRouter check
    try:
        import httpx
        start = time.time()
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get("https://openrouter.ai/api/v1/models",
                                   headers={"Authorization": f"Bearer {settings.OPENROUTER_API_KEY}"})
        latency = (time.time() - start) * 1000
        health["checks"]["openrouter"] = {
            "status": "healthy" if resp.status_code == 200 else "degraded",
            "latency_ms": round(latency, 2),
        }
    except Exception as e:
        health["checks"]["openrouter"] = {"status": "unhealthy", "error": str(e)}

    return health