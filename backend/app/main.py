"""
MT Expert Optimizer - FastAPI Main Application
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from prometheus_client import make_asgi_app
import time
import logging

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1 import api_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events
    """
    # Startup
    logger.info("🚀 Starting MT Expert Optimizer API...")

    # Create database tables
    # Note: In production, use Alembic migrations instead
    if settings.DEBUG:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    logger.info("✅ Application started successfully")

    yield

    # Shutdown
    logger.info("👋 Shutting down MT Expert Optimizer API...")
    await engine.dispose()


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="Automated MT4/MT5 Expert Advisor Optimization Platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)


# ===========================================
# Middleware
# ===========================================

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# ===========================================
# Exception Handlers
# ===========================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "type": "internal_error"
        }
    )


# ===========================================
# Routers
# ===========================================

# API v1 routes
app.include_router(api_router, prefix="/api/v1")


# Prometheus metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


# ===========================================
# Root Endpoints
# ===========================================

@app.get("/")
async def root():
    """
    API root endpoint
    """
    return {
        "name": settings.APP_NAME,
        "version": "1.0.0",
        "status": "operational",
        "docs": "/api/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for load balancers
    """
    return {
        "status": "healthy",
        "environment": settings.APP_ENV,
        "timestamp": time.time()
    }


@app.get("/ready")
async def readiness_check():
    """
    Readiness check for Kubernetes
    """
    # TODO: Add actual health checks (DB, Redis, etc.)
    return {
        "status": "ready",
        "checks": {
            "database": "ok",
            "redis": "ok",
            "celery": "ok"
        }
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
        workers=settings.API_WORKERS if not settings.API_RELOAD else 1,
        log_level=settings.LOG_LEVEL.lower()
    )
