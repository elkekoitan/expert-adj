"""
Authentication endpoints
"""
from fastapi import APIRouter

router = APIRouter()


@router.post("/register")
async def register():
    """Register new user"""
    return {"message": "Registration endpoint - TBD"}


@router.post("/login")
async def login():
    """User login"""
    return {"message": "Login endpoint - TBD"}


@router.post("/refresh")
async def refresh_token():
    """Refresh access token"""
    return {"message": "Refresh token endpoint - TBD"}


@router.post("/logout")
async def logout():
    """User logout"""
    return {"message": "Logout endpoint - TBD"}
