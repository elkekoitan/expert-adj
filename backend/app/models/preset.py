"""
Parameter Preset models for Expert Advisors
"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class EAParameterPreset(BaseModel):
    """
    Saved parameter configuration preset for an EA
    Users can save different parameter sets for backtesting/optimization
    """

    __tablename__ = "ea_parameter_presets"

    ea_version_id = Column(
        UUID(as_uuid=True), ForeignKey("ea_versions.id"), nullable=False
    )
    organization_id = Column(
        UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Store all parameter values as JSON
    # Format: {"MaxCascadeRobots": 5, "TriggerLevel": 2, ...}
    parameter_values = Column(JSONB, nullable=False, default={})

    # Tags for categorization (e.g., "aggressive", "conservative", "scalping")
    tags = Column(JSONB, default=[])

    # Performance metrics if this preset was backtested
    performance_metrics = Column(JSONB, default={})

    # Mark as template (shared across organization)
    is_template = Column(Boolean, default=False)
    is_public = Column(Boolean, default=False)

    # Favorite for quick access
    is_favorite = Column(Boolean, default=False)

    # Relationships
    ea_version = relationship("EAVersion", backref="presets")
    user = relationship("User", backref="ea_presets")
    organization = relationship("Organization", backref="ea_presets")


class EAParameterTemplate(BaseModel):
    """
    Reusable parameter templates across different EAs
    Useful for common strategies that can be applied to multiple EAs
    """

    __tablename__ = "ea_parameter_templates"

    organization_id = Column(
        UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True
    )
    creator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)

    # Strategy category (e.g., "Martingale", "Grid Trading", "Scalping")
    strategy_type = Column(String(100), nullable=True, index=True)

    # Template parameter rules
    # Format: {"RiskPercent": {"type": "double", "default": 2.0, "min": 0.5, "max": 5.0}, ...}
    parameter_schema = Column(JSONB, nullable=False, default={})

    # Suggested values for different risk levels
    # Format: {"conservative": {...}, "moderate": {...}, "aggressive": {...}}
    risk_profiles = Column(JSONB, default={})

    # Tags for search/filter
    tags = Column(JSONB, default=[])

    is_public = Column(Boolean, default=False)
    usage_count = Column(Integer, default=0)

    # Relationships
    creator = relationship("User", backref="parameter_templates")
    organization = relationship("Organization", backref="parameter_templates")


class EAParameterComparison(BaseModel):
    """
    Store parameter comparison sessions for analysis
    Users can compare multiple presets side-by-side
    """

    __tablename__ = "ea_parameter_comparisons"

    ea_version_id = Column(
        UUID(as_uuid=True), ForeignKey("ea_versions.id"), nullable=False
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # List of preset IDs being compared
    preset_ids = Column(JSONB, nullable=False, default=[])

    # Comparison notes and highlights
    notes = Column(Text, nullable=True)
    highlights = Column(JSONB, default={})

    # Recommendation based on comparison
    recommended_preset_id = Column(UUID(as_uuid=True), nullable=True)

    # Relationships
    ea_version = relationship("EAVersion", backref="parameter_comparisons")
    user = relationship("User", backref="parameter_comparisons")
