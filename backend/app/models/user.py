"""
User and Organization models
"""
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Organization(BaseModel):
    """
    Organization/Tenant model
    """

    __tablename__ = "organizations"

    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    settings = Column(JSONB, default={})

    # Relationships
    users = relationship("User", back_populates="organization")
    expert_advisors = relationship("ExpertAdvisor", back_populates="organization")


class User(BaseModel):
    """
    User model
    """

    __tablename__ = "users"

    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)

    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    # 2FA
    totp_secret = Column(String(255), nullable=True)
    is_2fa_enabled = Column(Boolean, default=False)

    # Quotas and limits
    max_eas = Column(Integer, default=5)
    max_backtests_per_month = Column(Integer, default=100)
    max_optimizations_per_month = Column(Integer, default=10)

    # Metadata
    settings = Column(JSONB, default={})
    last_login_at = Column(String, nullable=True)

    # Relationships
    organization = relationship("Organization", back_populates="users")
    expert_advisors = relationship("ExpertAdvisor", back_populates="owner")
    trading_accounts = relationship("TradingAccount", back_populates="owner")
