"""
API v1 Router
"""
from fastapi import APIRouter

from app.api.v1 import (
    health,
    auth,
    expert_advisors,
    presets,
    optimizations,
    backtests,
    trading,
)
# Use updated accounts
from app.api.v1 import accounts_updated as accounts
from app.api.v1 import strategy_presets

api_router = APIRouter()

# Include sub-routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(expert_advisors.router, prefix="/eas", tags=["expert-advisors"])
api_router.include_router(presets.router, prefix="/presets", tags=["presets"])
api_router.include_router(optimizations.router, prefix="/optimizations", tags=["optimizations"])
api_router.include_router(backtests.router, prefix="/backtests", tags=["backtests"])
api_router.include_router(trading.router, prefix="/trading", tags=["trading"])
api_router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
api_router.include_router(strategy_presets.router)
