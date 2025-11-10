"""
API v1 Router
"""
from fastapi import APIRouter

from app.api.v1 import health, auth, expert_advisors, optimizations, backtests, trading, accounts

api_router = APIRouter()

# Include sub-routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(expert_advisors.router, prefix="/eas", tags=["expert-advisors"])
api_router.include_router(optimizations.router, prefix="/optimizations", tags=["optimizations"])
api_router.include_router(backtests.router, prefix="/backtests", tags=["backtests"])
api_router.include_router(trading.router, prefix="/trading", tags=["trading"])
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
