"""
Optimization and backtest models
"""
from sqlalchemy import Column, String, ForeignKey, Integer, Boolean, Numeric, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class OptimizationSession(BaseModel):
    """
    Optimization session
    """

    __tablename__ = "optimization_sessions"

    ea_version_id = Column(UUID(as_uuid=True), ForeignKey("ea_versions.id"), nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    name = Column(String(255), nullable=True)

    # Configuration
    symbols = Column(ARRAY(String), nullable=False)
    timeframes = Column(ARRAY(String), nullable=False)
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)

    optimization_method = Column(String(50), nullable=False)  # grid, genetic, bayesian, random
    target_metric = Column(String(50), nullable=False, default="profit_factor")

    # Walk-forward config
    walk_forward_enabled = Column(Boolean, default=False)
    wf_config = Column(JSONB, default={})

    # Status
    status = Column(String(50), nullable=False, default="pending")  # pending, running, completed, failed, cancelled

    # Results
    total_iterations = Column(Integer, default=0)
    completed_iterations = Column(Integer, default=0)
    best_parameters = Column(JSONB, default={})
    best_score = Column(Numeric(15, 4), nullable=True)

    # Timing
    started_at = Column(String, nullable=True)
    completed_at = Column(String, nullable=True)

    # Metadata
    metadata = Column(JSONB, default={})
    error_message = Column(String, nullable=True)

    # Relationships
    ea_version = relationship("EAVersion", back_populates="optimization_sessions")
    backtest_results = relationship("BacktestResult", back_populates="optimization_session", cascade="all, delete-orphan")


class BacktestResult(BaseModel):
    """
    Individual backtest result
    """

    __tablename__ = "backtest_results"

    optimization_session_id = Column(UUID(as_uuid=True), ForeignKey("optimization_sessions.id"), nullable=True)
    ea_version_id = Column(UUID(as_uuid=True), ForeignKey("ea_versions.id"), nullable=False)

    # Test configuration
    symbol = Column(String(20), nullable=False)
    timeframe = Column(String(10), nullable=False)
    test_from = Column(Date, nullable=False)
    test_to = Column(Date, nullable=False)
    parameters = Column(JSONB, nullable=False)

    # Walk-forward flags
    is_training = Column(Boolean, default=False)
    is_oos = Column(Boolean, default=False)

    # Test environment
    initial_deposit = Column(Numeric(15, 2), default=10000)
    leverage = Column(Integer, default=100)
    modeling_quality = Column(Numeric(5, 2), nullable=True)

    # Performance metrics
    net_profit = Column(Numeric(15, 2), nullable=True)
    gross_profit = Column(Numeric(15, 2), nullable=True)
    gross_loss = Column(Numeric(15, 2), nullable=True)
    profit_factor = Column(Numeric(10, 4), nullable=True)
    expected_payoff = Column(Numeric(15, 2), nullable=True)

    # Trade statistics
    total_trades = Column(Integer, default=0)
    winning_trades = Column(Integer, default=0)
    losing_trades = Column(Integer, default=0)
    win_rate = Column(Numeric(5, 2), nullable=True)

    largest_win = Column(Numeric(15, 2), nullable=True)
    largest_loss = Column(Numeric(15, 2), nullable=True)
    average_win = Column(Numeric(15, 2), nullable=True)
    average_loss = Column(Numeric(15, 2), nullable=True)

    # Risk metrics
    max_drawdown = Column(Numeric(15, 2), nullable=True)
    max_drawdown_percent = Column(Numeric(5, 2), nullable=True)
    relative_drawdown = Column(Numeric(5, 2), nullable=True)

    sharpe_ratio = Column(Numeric(10, 4), nullable=True)
    sortino_ratio = Column(Numeric(10, 4), nullable=True)
    calmar_ratio = Column(Numeric(10, 4), nullable=True)
    recovery_factor = Column(Numeric(10, 4), nullable=True)

    # Score
    composite_score = Column(Numeric(10, 4), nullable=True)

    # Report files
    report_html_path = Column(String(500), nullable=True)
    report_xml_path = Column(String(500), nullable=True)
    trades_csv_path = Column(String(500), nullable=True)

    # Metadata
    terminal_build = Column(String(50), nullable=True)
    data_version = Column(String(50), nullable=True)
    metadata = Column(JSONB, default={})

    # Relationships
    optimization_session = relationship("OptimizationSession", back_populates="backtest_results")


class OptimizationBatch(BaseModel):
    """
    Batch of optimization runs for tracking
    """

    __tablename__ = "optimization_batches"

    session_id = Column(UUID(as_uuid=True), ForeignKey("optimization_sessions.id"), nullable=False)

    algorithm = Column(String(50), nullable=False)
    parameter_space = Column(JSONB, nullable=False)

    status = Column(String(50), nullable=False, default="pending")
    statistics = Column(JSONB, default={})
