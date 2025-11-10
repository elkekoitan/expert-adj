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

    # Social relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    following = relationship("UserFollow", foreign_keys="UserFollow.follower_id", back_populates="follower", cascade="all, delete-orphan")
    followers = relationship("UserFollow", foreign_keys="UserFollow.following_id", back_populates="following", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    sent_messages = relationship("DirectMessage", foreign_keys="DirectMessage.sender_id", back_populates="sender", cascade="all, delete-orphan")
    received_messages = relationship("DirectMessage", foreign_keys="DirectMessage.recipient_id", back_populates="recipient", cascade="all, delete-orphan")
    configurations = relationship("EAConfiguration", back_populates="user", cascade="all, delete-orphan")
    owned_workspaces = relationship("Workspace", back_populates="owner", cascade="all, delete-orphan")
    workspace_memberships = relationship("WorkspaceMember", back_populates="user", cascade="all, delete-orphan")
    badges = relationship("UserBadge", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user")
    oauth_connections = relationship("OAuthConnection", back_populates="user", cascade="all, delete-orphan")
