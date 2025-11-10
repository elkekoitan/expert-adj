"""
Pydantic schemas for social features
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, UUID4


# User Profile Schemas

class UserProfileBase(BaseModel):
    bio: Optional[str] = None
    website: Optional[str] = None
    twitter: Optional[str] = None
    linkedin: Optional[str] = None
    experience_level: Optional[str] = None
    preferred_markets: Optional[List[str]] = []
    risk_tolerance: Optional[str] = None
    trading_style: Optional[str] = None


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(UserProfileBase):
    profile_visibility: Optional[str] = None
    show_activity: Optional[bool] = None
    show_in_search: Optional[bool] = None


class UserProfileResponse(UserProfileBase):
    id: UUID4
    user_id: UUID4
    profile_visibility: str
    show_activity: bool
    show_in_search: bool
    reputation_score: int
    followers_count: int
    following_count: int
    eas_uploaded: int
    configs_shared: int
    is_verified: bool
    verification_date: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# Follow Schemas

class UserFollowCreate(BaseModel):
    following_id: UUID4


class UserFollowResponse(BaseModel):
    id: UUID4
    follower_id: UUID4
    following_id: UUID4
    created_at: str

    class Config:
        from_attributes = True


# Comment Schemas

class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)


class CommentCreate(CommentBase):
    commentable_type: str
    commentable_id: UUID4
    parent_comment_id: Optional[UUID4] = None


class CommentUpdate(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000)


class CommentResponse(CommentBase):
    id: UUID4
    user_id: UUID4
    commentable_type: str
    commentable_id: UUID4
    parent_comment_id: Optional[UUID4]
    is_hidden: bool
    is_deleted: bool
    deleted_at: Optional[str]
    likes_count: int
    replies_count: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# Like Schemas

class LikeCreate(BaseModel):
    likeable_type: str
    likeable_id: UUID4


class LikeResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    likeable_type: str
    likeable_id: UUID4
    created_at: str

    class Config:
        from_attributes = True


# Notification Schemas

class NotificationBase(BaseModel):
    type: str
    title: str
    content: Optional[str] = None
    data: Optional[dict] = {}
    action_url: Optional[str] = None


class NotificationCreate(NotificationBase):
    user_id: UUID4


class NotificationUpdate(BaseModel):
    is_read: bool


class NotificationResponse(NotificationBase):
    id: UUID4
    user_id: UUID4
    is_read: bool
    read_at: Optional[str]
    created_at: str

    class Config:
        from_attributes = True


# Direct Message Schemas

class DirectMessageBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=10000)
    attachments: Optional[List[dict]] = []


class DirectMessageCreate(DirectMessageBase):
    recipient_id: UUID4


class DirectMessageResponse(DirectMessageBase):
    id: UUID4
    sender_id: UUID4
    recipient_id: UUID4
    is_read: bool
    read_at: Optional[str]
    created_at: str

    class Config:
        from_attributes = True


# Conversation Schema

class ConversationResponse(BaseModel):
    other_user_id: UUID4
    other_user_name: str
    last_message: Optional[DirectMessageResponse]
    unread_count: int
