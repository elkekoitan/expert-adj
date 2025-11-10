"""
EA Parameter Preset endpoints
"""

from typing import List, Optional
from uuid import UUID

from app.core.database import get_db
from app.models.preset import (
    EAParameterComparison,
    EAParameterPreset,
    EAParameterTemplate,
)
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


# ==================== Pydantic Schemas ====================


class PresetCreate(BaseModel):
    """Schema for creating a new preset"""

    ea_version_id: UUID
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    parameter_values: dict = Field(..., description="Parameter name -> value mapping")
    tags: List[str] = Field(default_factory=list)
    is_template: bool = False
    is_public: bool = False


class PresetUpdate(BaseModel):
    """Schema for updating a preset"""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    parameter_values: Optional[dict] = None
    tags: Optional[List[str]] = None
    is_favorite: Optional[bool] = None
    performance_metrics: Optional[dict] = None


class PresetResponse(BaseModel):
    """Schema for preset response"""

    id: UUID
    ea_version_id: UUID
    user_id: UUID
    name: str
    description: Optional[str]
    parameter_values: dict
    tags: List[str]
    is_template: bool
    is_public: bool
    is_favorite: bool
    performance_metrics: dict
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class TemplateCreate(BaseModel):
    """Schema for creating a parameter template"""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    strategy_type: Optional[str] = None
    parameter_schema: dict = Field(..., description="Parameter definitions")
    risk_profiles: dict = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)
    is_public: bool = False


class ComparisonCreate(BaseModel):
    """Schema for creating a parameter comparison"""

    ea_version_id: UUID
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    preset_ids: List[UUID] = Field(..., min_items=2, max_items=10)
    notes: Optional[str] = None


# ==================== Preset Endpoints ====================


@router.post("/", response_model=PresetResponse, status_code=201)
async def create_preset(
    preset: PresetCreate,
    db: AsyncSession = Depends(get_db),
    # current_user = Depends(get_current_user)  # TODO: Add auth
):
    """
    Create a new parameter preset

    Allows users to save their EA parameter configurations for:
    - Quick parameter switching
    - Strategy comparison
    - Backtesting different setups
    """
    # TODO: Verify EA version exists
    # TODO: Validate parameter_values against EA parameter schema

    new_preset = EAParameterPreset(
        ea_version_id=preset.ea_version_id,
        # user_id=current_user.id,
        # organization_id=current_user.organization_id,
        name=preset.name,
        description=preset.description,
        parameter_values=preset.parameter_values,
        tags=preset.tags,
        is_template=preset.is_template,
        is_public=preset.is_public,
    )

    db.add(new_preset)
    await db.commit()
    await db.refresh(new_preset)

    return new_preset


@router.get("/", response_model=List[PresetResponse])
async def list_presets(
    ea_version_id: Optional[UUID] = Query(None, description="Filter by EA version"),
    tags: Optional[List[str]] = Query(None, description="Filter by tags"),
    is_template: Optional[bool] = Query(None, description="Filter templates"),
    is_favorite: Optional[bool] = Query(None, description="Filter favorites"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    # current_user = Depends(get_current_user)
):
    """
    List parameter presets

    Supports filtering by:
    - EA version
    - Tags (strategy type, risk level, etc.)
    - Template/favorite status
    """
    from sqlalchemy import select

    query = select(EAParameterPreset)

    # TODO: Filter by user/organization

    if ea_version_id:
        query = query.where(EAParameterPreset.ea_version_id == ea_version_id)

    if is_template is not None:
        query = query.where(EAParameterPreset.is_template == is_template)

    if is_favorite is not None:
        query = query.where(EAParameterPreset.is_favorite == is_favorite)

    query = query.limit(limit).offset(offset)

    result = await db.execute(query)
    presets = result.scalars().all()

    return presets


@router.get("/{preset_id}", response_model=PresetResponse)
async def get_preset(
    preset_id: UUID,
    db: AsyncSession = Depends(get_db),
    # current_user = Depends(get_current_user)
):
    """
    Get a specific preset by ID
    """
    from sqlalchemy import select

    result = await db.execute(
        select(EAParameterPreset).where(EAParameterPreset.id == preset_id)
    )
    preset = result.scalar_one_or_none()

    if not preset:
        raise HTTPException(status_code=404, detail="Preset not found")

    # TODO: Check user has access to this preset

    return preset


@router.put("/{preset_id}", response_model=PresetResponse)
async def update_preset(
    preset_id: UUID,
    updates: PresetUpdate,
    db: AsyncSession = Depends(get_db),
    # current_user = Depends(get_current_user)
):
    """
    Update a preset

    Allows updating:
    - Name and description
    - Parameter values
    - Tags and favorite status
    - Performance metrics (from backtest results)
    """
    from sqlalchemy import select

    result = await db.execute(
        select(EAParameterPreset).where(EAParameterPreset.id == preset_id)
    )
    preset = result.scalar_one_or_none()

    if not preset:
        raise HTTPException(status_code=404, detail="Preset not found")

    # TODO: Check user owns this preset

    # Update fields
    update_data = updates.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(preset, field, value)

    await db.commit()
    await db.refresh(preset)

    return preset


@router.delete("/{preset_id}", status_code=204)
async def delete_preset(
    preset_id: UUID,
    db: AsyncSession = Depends(get_db),
    # current_user = Depends(get_current_user)
):
    """
    Delete a preset
    """
    from sqlalchemy import delete, select

    result = await db.execute(
        select(EAParameterPreset).where(EAParameterPreset.id == preset_id)
    )
    preset = result.scalar_one_or_none()

    if not preset:
        raise HTTPException(status_code=404, detail="Preset not found")

    # TODO: Check user owns this preset

    await db.execute(delete(EAParameterPreset).where(EAParameterPreset.id == preset_id))
    await db.commit()

    return None


@router.post("/{preset_id}/clone", response_model=PresetResponse, status_code=201)
async def clone_preset(
    preset_id: UUID,
    name: str = Query(..., description="Name for the cloned preset"),
    db: AsyncSession = Depends(get_db),
    # current_user = Depends(get_current_user)
):
    """
    Clone an existing preset

    Useful for:
    - Creating variations of successful strategies
    - Testing small parameter changes
    - Copying public presets to personal collection
    """
    from sqlalchemy import select

    result = await db.execute(
        select(EAParameterPreset).where(EAParameterPreset.id == preset_id)
    )
    original = result.scalar_one_or_none()

    if not original:
        raise HTTPException(status_code=404, detail="Preset not found")

    # Create clone
    cloned = EAParameterPreset(
        ea_version_id=original.ea_version_id,
        # user_id=current_user.id,
        # organization_id=current_user.organization_id,
        name=name,
        description=f"Cloned from: {original.name}",
        parameter_values=original.parameter_values.copy(),
        tags=original.tags.copy() if original.tags else [],
        is_template=False,
        is_public=False,
    )

    db.add(cloned)
    await db.commit()
    await db.refresh(cloned)

    return cloned


# ==================== Template Endpoints ====================


@router.post("/templates/", status_code=201)
async def create_template(
    template: TemplateCreate,
    db: AsyncSession = Depends(get_db),
    # current_user = Depends(get_current_user)
):
    """
    Create a reusable parameter template

    Templates are strategy blueprints that can be:
    - Applied across multiple EAs
    - Shared with team/organization
    - Used as starting points for optimization
    """
    new_template = EAParameterTemplate(
        # creator_id=current_user.id,
        # organization_id=current_user.organization_id,
        name=template.name,
        description=template.description,
        strategy_type=template.strategy_type,
        parameter_schema=template.parameter_schema,
        risk_profiles=template.risk_profiles,
        tags=template.tags,
        is_public=template.is_public,
    )

    db.add(new_template)
    await db.commit()
    await db.refresh(new_template)

    return new_template


@router.get("/templates/")
async def list_templates(
    strategy_type: Optional[str] = Query(None),
    tags: Optional[List[str]] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """
    List parameter templates
    """
    from sqlalchemy import select

    query = select(EAParameterTemplate)

    if strategy_type:
        query = query.where(EAParameterTemplate.strategy_type == strategy_type)

    query = query.limit(limit).offset(offset)

    result = await db.execute(query)
    templates = result.scalars().all()

    return templates


# ==================== Comparison Endpoints ====================


@router.post("/comparisons/", status_code=201)
async def create_comparison(
    comparison: ComparisonCreate,
    db: AsyncSession = Depends(get_db),
    # current_user = Depends(get_current_user)
):
    """
    Create a parameter comparison session

    Compare multiple presets side-by-side to:
    - Analyze performance differences
    - Identify optimal parameters
    - Document strategy evolution
    """
    # TODO: Verify all preset IDs exist and belong to the EA version

    new_comparison = EAParameterComparison(
        ea_version_id=comparison.ea_version_id,
        # user_id=current_user.id,
        name=comparison.name,
        description=comparison.description,
        preset_ids=comparison.preset_ids,
        notes=comparison.notes,
    )

    db.add(new_comparison)
    await db.commit()
    await db.refresh(new_comparison)

    return new_comparison


@router.get("/comparisons/{comparison_id}")
async def get_comparison(
    comparison_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Get comparison details with all preset data
    """
    from sqlalchemy import select

    result = await db.execute(
        select(EAParameterComparison).where(EAParameterComparison.id == comparison_id)
    )
    comparison = result.scalar_one_or_none()

    if not comparison:
        raise HTTPException(status_code=404, detail="Comparison not found")

    # TODO: Fetch and return full preset data for each preset_id

    return comparison
