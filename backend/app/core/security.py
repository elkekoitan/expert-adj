"""
Security utilities for authentication and authorization
"""

import secrets
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db

# Bearer token security
security = HTTPBearer()


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt

    Args:
        password: Plain text password

    Returns:
        Hashed password
    """
    # Bcrypt has a 72-byte limit, truncate if necessary
    password_bytes = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash

    Args:
        plain_password: Plain text password
        hashed_password: Hashed password from database

    Returns:
        True if password matches
    """
    # Bcrypt has a 72-byte limit, truncate if necessary
    password_bytes = plain_password.encode("utf-8")[:72]
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create JWT access token

    Args:
        data: Payload data (user_id, email, etc.)
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire, "iat": datetime.utcnow(), "type": "access"})

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Create JWT refresh token (longer expiration)

    Args:
        data: Payload data (user_id, email, etc.)

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire, "iat": datetime.utcnow(), "type": "refresh"})

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and verify JWT token

    Args:
        token: JWT token string

    Returns:
        Decoded payload or None if invalid
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def generate_api_key() -> str:
    """
    Generate a random API key

    Returns:
        Random API key string
    """
    return secrets.token_urlsafe(32)


def encrypt_password(password: str, key: Optional[str] = None) -> str:
    """
    Encrypt password for storage (for MT5 accounts, etc.)
    Uses Fernet symmetric encryption

    Args:
        password: Plain text password
        key: Optional encryption key (uses SECRET_KEY if not provided)

    Returns:
        Encrypted password
    """
    import base64
    import hashlib

    from cryptography.fernet import Fernet

    # Generate key from settings.SECRET_KEY if not provided
    if key is None:
        key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()

    # Fernet requires base64 encoded key
    fernet_key = base64.urlsafe_b64encode(key)
    cipher = Fernet(fernet_key)

    encrypted = cipher.encrypt(password.encode())
    return encrypted.decode()


def decrypt_password(encrypted_password: str, key: Optional[str] = None) -> str:
    """
    Decrypt password

    Args:
        encrypted_password: Encrypted password string
        key: Optional encryption key (uses SECRET_KEY if not provided)

    Returns:
        Decrypted plain text password
    """
    import base64
    import hashlib

    from cryptography.fernet import Fernet

    # Generate key from settings.SECRET_KEY if not provided
    if key is None:
        key = hashlib.sha256(settings.SECRET_KEY.encode()).digest()

    # Fernet requires base64 encoded key
    fernet_key = base64.urlsafe_b64encode(key)
    cipher = Fernet(fernet_key)

    decrypted = cipher.decrypt(encrypted_password.encode())
    return decrypted.decode()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
):
    """
    Get current authenticated user from JWT token

    Args:
        credentials: Bearer token from request header
        db: Database session

    Returns:
        User object

    Raises:
        HTTPException: If token is invalid or user not found
    """
    from sqlalchemy import select

    from app.models.user import User

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials
    payload = decode_token(token)

    if payload is None:
        raise credentials_exception

    # Check token type
    if payload.get("type") != "access":
        raise credentials_exception

    # Get user ID from payload
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    # Fetch user from database
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive"
        )

    return user


async def get_current_active_user(current_user=Depends(get_current_user)):
    """
    Ensure user is active

    Args:
        current_user: Current user from get_current_user

    Returns:
        Active user object

    Raises:
        HTTPException: If user is not active
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


async def get_current_superuser(current_user=Depends(get_current_user)):
    """
    Ensure user is superuser

    Args:
        current_user: Current user from get_current_user

    Returns:
        Superuser object

    Raises:
        HTTPException: If user is not superuser
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges"
        )
    return current_user


def validate_password(password: str) -> bool:
    """
    Validate password against security policy

    Args:
        password: Plain text password

    Returns:
        True if password meets requirements

    Raises:
        ValueError: If password doesn't meet requirements
    """
    if len(password) < settings.MIN_PASSWORD_LENGTH:
        raise ValueError(
            f"Password must be at least {settings.MIN_PASSWORD_LENGTH} characters"
        )

    if settings.REQUIRE_UPPERCASE and not any(c.isupper() for c in password):
        raise ValueError("Password must contain at least one uppercase letter")

    if settings.REQUIRE_NUMBER and not any(c.isdigit() for c in password):
        raise ValueError("Password must contain at least one number")

    if settings.REQUIRE_SPECIAL_CHAR and not any(
        c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password
    ):
        raise ValueError("Password must contain at least one special character")

    return True


class PasswordGenerator:
    """Generate secure random passwords"""

    @staticmethod
    def generate(length: int = 16, include_special: bool = True) -> str:
        """
        Generate a random secure password

        Args:
            length: Password length
            include_special: Include special characters

        Returns:
            Random password string
        """
        import string

        chars = string.ascii_letters + string.digits
        if include_special:
            chars += "!@#$%^&*()_+-="

        password = "".join(secrets.choice(chars) for _ in range(length))
        return password
