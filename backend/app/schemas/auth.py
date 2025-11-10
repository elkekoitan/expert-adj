"""
Authentication and OAuth schemas
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field, UUID4


# OAuth Schemas

class OAuthConnectionResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    provider: str
    provider_user_id: str
    profile_data: Dict[str, Any]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class GoogleOAuthInitiate(BaseModel):
    """Request to initiate Google OAuth flow"""
    pass


class GoogleOAuthCallback(BaseModel):
    """Google OAuth callback data"""
    code: str
    state: str


class GoogleOAuthResponse(BaseModel):
    """Response after successful Google OAuth"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: "UserResponse"  # Forward reference


# User Auth Schemas

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=12)
    full_name: Optional[str] = None


class UserResponse(BaseModel):
    id: UUID4
    email: str
    username: str
    full_name: Optional[str]
    is_active: bool
    is_verified: bool
    is_superuser: bool
    is_2fa_enabled: bool
    created_at: str

    class Config:
        from_attributes = True


class UserWithProfile(UserResponse):
    """Extended user response with profile"""
    profile: Optional["UserProfileResponse"] = None  # Forward reference


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenRefresh(BaseModel):
    refresh_token: str


# 2FA Schemas

class TwoFactorSetup(BaseModel):
    """2FA setup response"""
    secret: str
    qr_code: str  # Base64 encoded QR code image
    backup_codes: list[str]


class TwoFactorVerify(BaseModel):
    """Verify 2FA code"""
    code: str = Field(..., min_length=6, max_length=6)


class TwoFactorDisable(BaseModel):
    """Disable 2FA"""
    password: str
    code: str = Field(..., min_length=6, max_length=6)


# Password Management

class PasswordChange(BaseModel):
    """Change password"""
    current_password: str
    new_password: str = Field(..., min_length=12)


class PasswordReset(BaseModel):
    """Reset password with token"""
    token: str
    new_password: str = Field(..., min_length=12)


class PasswordResetRequest(BaseModel):
    """Request password reset"""
    email: EmailStr


# Audit Log Schema

class AuditLogResponse(BaseModel):
    id: UUID4
    user_id: Optional[UUID4]
    action: str
    resource_type: Optional[str]
    resource_id: Optional[UUID4]
    details: Optional[Dict[str, Any]]
    ip_address: Optional[str]
    user_agent: Optional[str]
    status: Optional[str]
    created_at: str

    class Config:
        from_attributes = True


class AuditLogQuery(BaseModel):
    """Query parameters for audit logs"""
    user_id: Optional[UUID4] = None
    action: Optional[str] = None
    resource_type: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    limit: int = Field(default=50, le=1000)
    offset: int = Field(default=0, ge=0)
