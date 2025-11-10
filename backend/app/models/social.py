"""
Social features models: profiles, follows, comments, likes, notifications
"""
from sqlalchemy import Column, String, ForeignKey, Boolean, Integer, Text, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class UserProfile(BaseModel):
    """
    Extended user profile with social and trading information
    """

    __tablename__ = "user_profiles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)

    # Bio & Social Links
    bio = Column(Text, nullable=True)
    website = Column(String(500), nullable=True)
    twitter = Column(String(100), nullable=True)
    linkedin = Column(String(100), nullable=True)

    # Trading Information
    experience_level = Column(String(20), nullable=True)  # beginner, intermediate, advanced, expert
    preferred_markets = Column(JSONB, default=[])  # ['forex', 'crypto', 'stocks']
    risk_tolerance = Column(String(20), nullable=True)  # low, medium, high
    trading_style = Column(String(50), nullable=True)  # scalper, day_trader, swing_trader, position_trader

    # Privacy Settings
    profile_visibility = Column(String(20), default="public")  # public, followers_only, private
    show_activity = Column(Boolean, default=True)
    show_in_search = Column(Boolean, default=True)

    # Statistics (cached from relationships)
    reputation_score = Column(Integer, default=0)
    followers_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    eas_uploaded = Column(Integer, default=0)
    configs_shared = Column(Integer, default=0)

    # Verification
    is_verified = Column(Boolean, default=False)
    verification_date = Column(String, nullable=True)

    # Relationships
    user = relationship("User", back_populates="profile", uselist=False)


class UserFollow(BaseModel):
    """
    User following relationship
    """

    __tablename__ = "user_follows"

    follower_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    following_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    following = relationship("User", foreign_keys=[following_id], back_populates="followers")

    __table_args__ = (
        CheckConstraint('follower_id != following_id', name='check_no_self_follow'),
    )


class Comment(BaseModel):
    """
    Comments on various resources (polymorphic)
    Can comment on EAs, configurations, etc.
    """

    __tablename__ = "comments"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Polymorphic association
    commentable_type = Column(String(50), nullable=False)  # 'ea', 'configuration', 'backtest'
    commentable_id = Column(UUID(as_uuid=True), nullable=False)

    content = Column(Text, nullable=False)
    parent_comment_id = Column(UUID(as_uuid=True), ForeignKey("comments.id", ondelete="CASCADE"), nullable=True)

    # Moderation
    is_hidden = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(String, nullable=True)

    # Engagement (cached)
    likes_count = Column(Integer, default=0)
    replies_count = Column(Integer, default=0)

    # Relationships
    user = relationship("User", back_populates="comments")
    parent = relationship("Comment", remote_side="Comment.id", back_populates="replies")
    replies = relationship("Comment", back_populates="parent", cascade="all, delete-orphan")


class Like(BaseModel):
    """
    Likes on various resources (polymorphic)
    Can like EAs, configurations, comments, etc.
    """

    __tablename__ = "likes"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Polymorphic association
    likeable_type = Column(String(50), nullable=False)  # 'ea', 'configuration', 'comment'
    likeable_id = Column(UUID(as_uuid=True), nullable=False)

    # Relationships
    user = relationship("User", back_populates="likes")


class Notification(BaseModel):
    """
    User notifications
    """

    __tablename__ = "notifications"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    type = Column(String(50), nullable=False)  # new_follower, comment_reply, like, etc.
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    data = Column(JSONB, default={})  # Additional data (user_id, ea_id, etc.)

    is_read = Column(Boolean, default=False)
    read_at = Column(String, nullable=True)

    # Action URL (for clickable notifications)
    action_url = Column(String(500), nullable=True)

    # Relationships
    user = relationship("User", back_populates="notifications")


class DirectMessage(BaseModel):
    """
    Direct messages between users
    """

    __tablename__ = "direct_messages"

    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    recipient_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    content = Column(Text, nullable=False)
    attachments = Column(JSONB, default=[])  # [{type: 'file', url: '...', name: '...'}]

    is_read = Column(Boolean, default=False)
    read_at = Column(String, nullable=True)

    # Soft delete per user
    is_deleted_by_sender = Column(Boolean, default=False)
    is_deleted_by_recipient = Column(Boolean, default=False)

    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    recipient = relationship("User", foreign_keys=[recipient_id], back_populates="received_messages")
