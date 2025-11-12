"""
Authentication endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.core.database import get_db
from app.models.user import User

router = APIRouter()


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: str
    password: str


async def authenticate_user(
    session: AsyncSession, email: str, password: str
) -> User | None:
    """
    Verilen email/parola ile kullanıcı doğrula.
    """
    result = await session.execute(
        User.__table__.select().where(User.email == email)
    )
    user = result.scalar_one_or_none()
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user


@router.post("/login", response_model=TokenResponse, summary="Kullanıcı girişi (JWT)")
async def login(
    data: LoginRequest,
    session: AsyncSession = Depends(get_db),
):
    """
    Basit email/parola ile login.
    Başarılı olursa JWT access_token döner.
    """
    user = await authenticate_user(session, data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect email or password",
        )

    token = security.create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
            "is_superuser": bool(getattr(user, "is_superuser", False)),
        }
    )
    return TokenResponse(access_token=token)
