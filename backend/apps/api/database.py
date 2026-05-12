from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool
from config import settings
import structlog
import socket
import ssl as ssl_module
import json
import urllib.request
from urllib.parse import urlparse

logger = structlog.get_logger(__name__)


def _resolve_db_url(db_url: str) -> tuple:
    """Resolve DB hostname via Google DNS-over-HTTPS if local DNS fails.
    Returns (resolved_url, ssl_context_or_string)."""
    parsed = urlparse(db_url)
    hostname = parsed.hostname

    # Create SSL context that accepts custom hostnames or IPs reliably
    ctx = ssl_module.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl_module.CERT_NONE

    # Test if local DNS can resolve
    try:
        socket.getaddrinfo(hostname, parsed.port or 6543, socket.AF_INET)
        logger.info("DNS resolved locally", host=hostname)
        return db_url, ctx
    except socket.gaierror:
        logger.warning("Local DNS failed, trying Google DNS", host=hostname)

    # Fallback: resolve via Google DNS-over-HTTPS
    try:
        req = urllib.request.Request(
            f"https://dns.google/resolve?name={hostname}&type=A",
            headers={"Accept": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())

        ip = None
        for answer in data.get("Answer", []):
            if answer.get("type") == 1:  # A record
                ip = answer["data"]
                break

        if ip:
            # Replace hostname with IP in URL
            resolved_url = db_url.replace(f"@{hostname}", f"@{ip}")
            logger.info("DNS resolved via Google", host=hostname, ip=ip)
            return resolved_url, ctx
    except Exception as e:
        logger.error("Google DNS fallback failed", error=str(e))

    # Last resort: return original with relaxed SSL
    return db_url, ctx


_resolved_url, _ssl_ctx = _resolve_db_url(settings.DATABASE_URL)


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    _resolved_url,
    echo=settings.DEBUG,
    poolclass=NullPool,
    connect_args={
        "ssl": _ssl_ctx,
        "prepared_statement_cache_size": 0,
        "server_settings": {
            "application_name": settings.APP_NAME,
        }
    },
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error("Database session error", error=str(e))
            raise
        finally:
            await session.close()


async def init_db():
    try:
        import models
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.warning(f"Failed to connect to database: {str(e)}")
        logger.warning("Application started without database connection.")


async def close_db():
    await engine.dispose()
    logger.info("Database connections closed")