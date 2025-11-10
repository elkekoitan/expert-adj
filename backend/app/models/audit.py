"""
Audit logging and OAuth connection models
"""
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class AuditLog(BaseModel):
    """
    Audit log for tracking all important actions
    """

    __tablename__ = "audit_logs"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    action = Column(String(100), nullable=False)  # login, user_create, ea_upload, etc.
    resource_type = Column(String(50), nullable=True)  # user, ea, configuration, etc.
    resource_id = Column(UUID(as_uuid=True), nullable=True)

    details = Column(JSONB, default={})  # Additional action details

    # Request metadata
    ip_address = Column(String(45), nullable=True)  # Support IPv6
    user_agent = Column(Text, nullable=True)

    status = Column(String(20), nullable=True)  # success, failure, error

    # Relationships
    user = relationship("User", back_populates="audit_logs")


class OAuthConnection(BaseModel):
    """
    OAuth provider connections (Google, GitHub, etc.)
    """

    __tablename__ = "oauth_connections"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    provider = Column(String(50), nullable=False)  # google, github, microsoft
    provider_user_id = Column(String(255), nullable=False)  # User ID from provider

    # Tokens (encrypted at application level)
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    expires_at = Column(String, nullable=True)

    # Profile data from provider
    profile_data = Column(JSONB, default={})  # name, email, avatar, etc.

    # Relationships
    user = relationship("User", back_populates="oauth_connections")
