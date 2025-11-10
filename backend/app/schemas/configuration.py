"""
Pydantic schemas for EA configurations and workspaces
"""
from typing import Optional, List, Dict, Any
from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field, UUID4


# EA Configuration Schemas

class EAConfigurationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    parameters: Dict[str, Any]
    symbol: Optional[str] = None
    timeframe: Optional[str] = None
    backtest_from: Optional[date] = None
    backtest_to: Optional[date] = None
    tags: Optional[List[str]] = []


class EAConfigurationCreate(EAConfigurationBase):
    ea_version_id: UUID4
    visibility: Optional[str] = "private"
    parent_config_id: Optional[UUID4] = None


class EAConfigurationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    visibility: Optional[str] = None
    tags: Optional[List[str]] = None


class EAConfigurationResponse(EAConfigurationBase):
    id: UUID4
    ea_version_id: UUID4
    user_id: UUID4
    visibility: str
    is_featured: bool

    # Performance metrics
    profit_factor: Optional[Decimal]
    win_rate: Optional[Decimal]
    total_trades: Optional[int]
    net_profit: Optional[Decimal]
    max_drawdown: Optional[Decimal]
    sharpe_ratio: Optional[Decimal]

    # Engagement
    likes_count: int
    uses_count: int
    forks_count: int
    views_count: int

    parent_config_id: Optional[UUID4]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class EAConfigurationWithAuthor(EAConfigurationResponse):
    """Extended response with author info"""
    author_name: str
    author_username: str
    author_avatar: Optional[str] = None


# Workspace Schemas

class WorkspaceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    visibility: Optional[str] = "private"
    settings: Optional[Dict[str, Any]] = {}


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceUpdate(WorkspaceBase):
    name: Optional[str] = Field(None, min_length=1, max_length=255)


class WorkspaceResponse(WorkspaceBase):
    id: UUID4
    owner_id: UUID4
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# Workspace Member Schemas

class WorkspaceMemberBase(BaseModel):
    role: str = "viewer"


class WorkspaceMemberCreate(WorkspaceMemberBase):
    user_id: UUID4


class WorkspaceMemberUpdate(BaseModel):
    role: str


class WorkspaceMemberResponse(WorkspaceMemberBase):
    id: UUID4
    workspace_id: UUID4
    user_id: UUID4
    joined_at: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class WorkspaceMemberWithUser(WorkspaceMemberResponse):
    """Extended response with user info"""
    user_name: str
    user_email: str
    user_avatar: Optional[str] = None


# Badge Schemas

class BadgeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    icon: Optional[str] = None
    category: Optional[str] = None
    criteria: Optional[Dict[str, Any]] = None
    display_order: int = 0
    is_active: bool = True


class BadgeCreate(BadgeBase):
    pass


class BadgeUpdate(BadgeBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    is_active: Optional[bool] = None


class BadgeResponse(BadgeBase):
    id: UUID4
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# User Badge Schemas

class UserBadgeResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    badge_id: UUID4
    badge_name: str
    badge_description: Optional[str]
    badge_icon: Optional[str]
    badge_category: Optional[str]
    earned_at: Optional[str]
    created_at: str

    class Config:
        from_attributes = True
