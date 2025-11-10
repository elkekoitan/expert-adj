"""
Database models
"""
from app.models.user import User, Organization
from app.models.expert_advisor import ExpertAdvisor, EAVersion, EAParameter, Dependency
from app.models.optimization import OptimizationSession, BacktestResult, OptimizationBatch
from app.models.trading import TradingAccount, LiveSession, Trade, Position
from app.models.instrument import Instrument
from app.models.social import UserProfile, UserFollow, Comment, Like, Notification, DirectMessage
from app.models.configuration import EAConfiguration, Workspace, WorkspaceMember, Badge, UserBadge
from app.models.audit import AuditLog, OAuthConnection

__all__ = [
    # Core
    "User",
    "Organization",
    # EA Models
    "ExpertAdvisor",
    "EAVersion",
    "EAParameter",
    "Dependency",
    # Optimization
    "OptimizationSession",
    "BacktestResult",
    "OptimizationBatch",
    # Trading
    "TradingAccount",
    "LiveSession",
    "Trade",
    "Position",
    "Instrument",
    # Social
    "UserProfile",
    "UserFollow",
    "Comment",
    "Like",
    "Notification",
    "DirectMessage",
    # Configuration & Workspace
    "EAConfiguration",
    "Workspace",
    "WorkspaceMember",
    # Gamification
    "Badge",
    "UserBadge",
    # Audit & OAuth
    "AuditLog",
    "OAuthConnection",
]
