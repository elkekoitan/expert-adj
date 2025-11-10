"""
Health check endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import redis.asyncio as aioredis

from app.core.database import get_db
from app.core.config import settings

router = APIRouter()


@router.get("/")
async def health_check():
    """
    Basic health check
    """
    return {"status": "healthy"}


@router.get("/detailed")
async def detailed_health_check(db: AsyncSession = Depends(get_db)):
    """
    Detailed health check including dependencies
    """
    checks = {
        "api": "healthy",
        "database": "unknown",
        "redis": "unknown",
    }

    # Check database
    try:
        result = await db.execute(text("SELECT 1"))
        if result:
            checks["database"] = "healthy"
    except Exception as e:
        checks["database"] = f"unhealthy: {str(e)}"

    # Check Redis
    try:
        redis_client = aioredis.from_url(settings.REDIS_URL)
        await redis_client.ping()
        checks["redis"] = "healthy"
        await redis_client.close()
    except Exception as e:
        checks["redis"] = f"unhealthy: {str(e)}"

    # Determine overall status
    all_healthy = all(status == "healthy" for status in checks.values())
    overall_status = "healthy" if all_healthy else "degraded"

    return {
        "status": overall_status,
        "checks": checks
    }
