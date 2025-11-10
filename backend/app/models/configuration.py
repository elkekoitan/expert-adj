"""
EA Configuration sharing models
"""
from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, Date, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class EAConfiguration(BaseModel):
    """
    Shareable EA configuration (parameter sets)
    """

    __tablename__ = "ea_configurations"

    ea_version_id = Column(UUID(as_uuid=True), ForeignKey("ea_versions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    name = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    parameters = Column(JSONB, nullable=False)  # Complete parameter set

    # Trading Context
    symbol = Column(String(20), nullable=True)
    timeframe = Column(String(10), nullable=True)
    backtest_from = Column(Date, nullable=True)
    backtest_to = Column(Date, nullable=True)

    # Performance Metrics (if backtested)
    profit_factor = Column(Numeric(10, 4), nullable=True)
    win_rate = Column(Numeric(5, 2), nullable=True)
    total_trades = Column(Integer, nullable=True)
    net_profit = Column(Numeric(15, 2), nullable=True)
    max_drawdown = Column(Numeric(15, 2), nullable=True)
    sharpe_ratio = Column(Numeric(10, 4), nullable=True)

    # Sharing Settings
    visibility = Column(String(20), default="private")  # public, unlisted, private, followers_only
    is_featured = Column(Boolean, default=False)  # Featured by admin

    # Engagement (cached)
    likes_count = Column(Integer, default=0)
    uses_count = Column(Integer, default=0)  # How many times imported
    forks_count = Column(Integer, default=0)  # How many times forked
    views_count = Column(Integer, default=0)

    # Fork Tracking
    parent_config_id = Column(UUID(as_uuid=True), ForeignKey("ea_configurations.id"), nullable=True)

    # Tags for discovery
    tags = Column(JSONB, default=[])

    # Relationships
    ea_version = relationship("EAVersion", back_populates="configurations")
    user = relationship("User", back_populates="configurations")
    parent = relationship("EAConfiguration", remote_side="EAConfiguration.id", back_populates="forks")
    forks = relationship("EAConfiguration", back_populates="parent", cascade="all, delete-orphan")


class Workspace(BaseModel):
    """
    Collaborative workspace for teams
    """

    __tablename__ = "workspaces"

    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    name = Column(String(255), nullable=False)
    description = Column(String, nullable=True)

    visibility = Column(String(20), default="private")  # public, private

    # Settings
    settings = Column(JSONB, default={})

    # Relationships
    owner = relationship("User", back_populates="owned_workspaces")
    members = relationship("WorkspaceMember", back_populates="workspace", cascade="all, delete-orphan")


class WorkspaceMember(BaseModel):
    """
    Workspace membership with roles
    """

    __tablename__ = "workspace_members"

    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    role = Column(String(20), default="viewer")  # owner, editor, viewer

    joined_at = Column(String, nullable=True)

    # Relationships
    workspace = relationship("Workspace", back_populates="members")
    user = relationship("User", back_populates="workspace_memberships")


class Badge(BaseModel):
    """
    Achievement badges
    """

    __tablename__ = "badges"

    name = Column(String(100), nullable=False, unique=True)
    description = Column(String, nullable=True)
    icon = Column(String(100), nullable=True)  # Icon name or URL
    category = Column(String(50), nullable=True)  # contributor, performance, community, special

    # Criteria for automatic awarding (JSON schema)
    criteria = Column(JSONB, nullable=True)

    # Display order
    display_order = Column(Integer, default=0)

    is_active = Column(Boolean, default=True)

    # Relationships
    user_badges = relationship("UserBadge", back_populates="badge", cascade="all, delete-orphan")


class UserBadge(BaseModel):
    """
    Badges earned by users
    """

    __tablename__ = "user_badges"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    badge_id = Column(UUID(as_uuid=True), ForeignKey("badges.id", ondelete="CASCADE"), nullable=False)

    earned_at = Column(String, nullable=True)

    # Relationships
    user = relationship("User", back_populates="badges")
    badge = relationship("Badge", back_populates="user_badges")
