"""
Live trading models
"""
from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class TradingAccount(BaseModel):
    """
    Trading account (demo or live)
    """

    __tablename__ = "trading_accounts"

    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    platform = Column(String(10), nullable=False)  # MT4 or MT5
    broker_server = Column(String(100), nullable=False)
    account_number = Column(String(50), nullable=False)
    account_type = Column(String(20), nullable=False, default="demo")  # demo or live

    label = Column(String(255), nullable=True)

    # Credentials (encrypted)
    encrypted_password = Column(String(500), nullable=True)

    is_active = Column(Boolean, default=True)
    is_connected = Column(Boolean, default=False)

    # Account info
    balance = Column(Numeric(15, 2), nullable=True)
    equity = Column(Numeric(15, 2), nullable=True)
    margin = Column(Numeric(15, 2), nullable=True)
    free_margin = Column(Numeric(15, 2), nullable=True)
    leverage = Column(Integer, nullable=True)
    currency = Column(String(10), default="USD")

    # Metadata
    last_heartbeat = Column(String, nullable=True)
    metadata = Column(JSONB, default={})

    # Relationships
    owner = relationship("User", back_populates="trading_accounts")
    live_sessions = relationship("LiveSession", back_populates="account", cascade="all, delete-orphan")


class LiveSession(BaseModel):
    """
    Live trading session
    """

    __tablename__ = "live_sessions"

    account_id = Column(UUID(as_uuid=True), ForeignKey("trading_accounts.id"), nullable=False)
    ea_version_id = Column(UUID(as_uuid=True), ForeignKey("ea_versions.id"), nullable=False)

    symbol = Column(String(20), nullable=False)
    timeframe = Column(String(10), nullable=False)
    parameters = Column(JSONB, nullable=False)

    # Status
    status = Column(String(50), nullable=False, default="pending")  # pending, running, paused, stopped, error

    # Performance
    initial_balance = Column(Numeric(15, 2), nullable=True)
    current_profit = Column(Numeric(15, 2), default=0)
    peak_profit = Column(Numeric(15, 2), default=0)
    current_drawdown = Column(Numeric(15, 2), default=0)
    max_drawdown = Column(Numeric(15, 2), default=0)

    total_trades = Column(Integer, default=0)
    winning_trades = Column(Integer, default=0)
    losing_trades = Column(Integer, default=0)

    # Risk management
    threshold_policy = Column(JSONB, default={})

    # Timing
    started_at = Column(String, nullable=True)
    stopped_at = Column(String, nullable=True)

    # Metadata
    metadata = Column(JSONB, default={})

    # Relationships
    account = relationship("TradingAccount", back_populates="live_sessions")
    trades = relationship("Trade", back_populates="session", cascade="all, delete-orphan")
    positions = relationship("Position", back_populates="session", cascade="all, delete-orphan")


class Trade(BaseModel):
    """
    Individual trade (closed position)
    """

    __tablename__ = "trades"

    session_id = Column(UUID(as_uuid=True), ForeignKey("live_sessions.id"), nullable=False)

    ticket = Column(Integer, nullable=False, index=True)
    symbol = Column(String(20), nullable=False)
    trade_type = Column(String(10), nullable=False)  # BUY, SELL

    volume = Column(Numeric(10, 2), nullable=False)
    open_price = Column(Numeric(15, 5), nullable=False)
    close_price = Column(Numeric(15, 5), nullable=False)

    stop_loss = Column(Numeric(15, 5), nullable=True)
    take_profit = Column(Numeric(15, 5), nullable=True)

    profit = Column(Numeric(15, 2), nullable=False)
    commission = Column(Numeric(15, 2), default=0)
    swap = Column(Numeric(15, 2), default=0)

    open_time = Column(String, nullable=False)
    close_time = Column(String, nullable=False)

    # Metadata
    comment = Column(String(255), nullable=True)
    metadata = Column(JSONB, default={})

    # Relationships
    session = relationship("LiveSession", back_populates="trades")


class Position(BaseModel):
    """
    Open position
    """

    __tablename__ = "positions"

    session_id = Column(UUID(as_uuid=True), ForeignKey("live_sessions.id"), nullable=False)

    ticket = Column(Integer, nullable=False, index=True)
    symbol = Column(String(20), nullable=False)
    position_type = Column(String(10), nullable=False)  # BUY, SELL

    volume = Column(Numeric(10, 2), nullable=False)
    open_price = Column(Numeric(15, 5), nullable=False)
    current_price = Column(Numeric(15, 5), nullable=True)

    stop_loss = Column(Numeric(15, 5), nullable=True)
    take_profit = Column(Numeric(15, 5), nullable=True)

    profit = Column(Numeric(15, 2), default=0)
    commission = Column(Numeric(15, 2), default=0)
    swap = Column(Numeric(15, 2), default=0)

    open_time = Column(String, nullable=False)

    # Metadata
    comment = Column(String(255), nullable=True)
    metadata = Column(JSONB, default={})

    # Relationships
    session = relationship("LiveSession", back_populates="positions")
