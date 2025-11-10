"""
Expert Advisor models
"""
from sqlalchemy import Column, String, ForeignKey, Boolean, Integer, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class ExpertAdvisor(BaseModel):
    """
    Expert Advisor (EA) main record
    """

    __tablename__ = "expert_advisors"

    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    platform = Column(String(10), nullable=False)  # MT4 or MT5
    tags = Column(JSONB, default=[])

    is_active = Column(Boolean, default=True)

    # Relationships
    organization = relationship("Organization", back_populates="expert_advisors")
    owner = relationship("User", back_populates="expert_advisors")
    versions = relationship("EAVersion", back_populates="expert_advisor", cascade="all, delete-orphan")


class EAVersion(BaseModel):
    """
    EA version with compiled file and source code
    """

    __tablename__ = "ea_versions"

    ea_id = Column(UUID(as_uuid=True), ForeignKey("expert_advisors.id"), nullable=False)

    version = Column(String(50), nullable=False)
    build_hash = Column(String(64), nullable=True, index=True)

    # File paths in S3
    compiled_file_path = Column(String(500), nullable=False)
    source_file_path = Column(String(500), nullable=True)

    # Metadata
    source_present = Column(Boolean, default=False)
    requires_sdk = Column(Boolean, default=False)
    compiled_at = Column(String, nullable=True)

    metadata = Column(JSONB, default={})

    # Relationships
    expert_advisor = relationship("ExpertAdvisor", back_populates="versions")
    parameters = relationship("EAParameter", back_populates="ea_version", cascade="all, delete-orphan")
    dependencies = relationship("Dependency", back_populates="ea_version", cascade="all, delete-orphan")
    optimization_sessions = relationship("OptimizationSession", back_populates="ea_version")


class EAParameter(BaseModel):
    """
    EA input parameters schema
    """

    __tablename__ = "ea_parameters"

    ea_version_id = Column(UUID(as_uuid=True), ForeignKey("ea_versions.id"), nullable=False)

    name = Column(String(255), nullable=False)
    parameter_type = Column(String(50), nullable=False)  # int, double, string, bool, enum
    default_value = Column(String(255), nullable=True)

    # For optimization
    min_value = Column(String(255), nullable=True)
    max_value = Column(String(255), nullable=True)
    step_value = Column(String(255), nullable=True)

    # For enum types
    enum_values = Column(JSONB, default=[])

    description = Column(Text, nullable=True)
    is_optimizable = Column(Boolean, default=True)

    # Relationships
    ea_version = relationship("EAVersion", back_populates="parameters")


class Dependency(BaseModel):
    """
    EA dependencies (indicators, includes, libraries)
    """

    __tablename__ = "dependencies"

    ea_version_id = Column(UUID(as_uuid=True), ForeignKey("ea_versions.id"), nullable=False)

    dependency_type = Column(String(50), nullable=False)  # indicator, include, library
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    checksum = Column(String(64), nullable=True)

    # Relationships
    ea_version = relationship("EAVersion", back_populates="dependencies")
