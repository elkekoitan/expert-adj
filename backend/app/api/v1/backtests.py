"""
Backtest endpoints - gerçek enqueue + liste + detay
"""
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.strategy import BacktestRun, StrategyPreset
from app.models.user import User

router = APIRouter()


class BacktestCreate(BaseModel):
    preset_id: UUID = Field(..., description="Kullanılacak StrategyPreset ID")
    date_from: str = Field(..., description="Backtest başlangıç tarihi, örn: 2020-01-01")
    date_to: str = Field(..., description="Backtest bitiş tarihi, örn: 2024-01-01")
    engine: str = Field(
        default="mt5_local",
        description="mt4_local / mt5_local / custom",
    )


class BacktestUpdate(BaseModel):
    status: Optional[str] = None
    metrics: Optional[dict] = None
    report_ref: Optional[str] = None


class BacktestResponse(BaseModel):
    id: UUID
    preset_id: Optional[UUID]
    symbol: str
    timeframe: str
    date_from: str
    date_to: str
    engine: str
    status: str
    metrics: Optional[dict]
    report_ref: Optional[str]

    class Config:
        from_attributes = True


@router.post(
    "/",
    response_model=BacktestResponse,
    status_code=status.HTTP_201_CREATED,
)
def enqueue_backtest(
    payload: BacktestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    StrategyPreset'e bağlı bir BacktestRun oluşturur (status=queued).
    Runner bu kayıtları okuyup çalıştıracak.
    """
    preset = (
        db.query(StrategyPreset)
        .filter(StrategyPreset.id == payload.preset_id)
        .first()
    )
    if not preset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preset not found",
        )

    run = BacktestRun(
        owner_id=current_user.id,
        organization_id=current_user.organization_id,
        preset_id=payload.preset_id,
        symbol=preset.symbol or "XAUUSD",
        timeframe=preset.timeframe or "M15",
        date_from=payload.date_from,
        date_to=payload.date_to,
        engine=payload.engine,
        parameters=preset.parameters or {},
        status="queued",
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


@router.get(
    "/",
    response_model=List[BacktestResponse],
)
def list_backtests(
    preset_id: Optional[UUID] = None,
    status_filter: Optional[str] = Query(None, alias="status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Kullanıcının backtestlerini (veya admin ise tamamını) döner.
    İsteğe bağlı preset_id ve status filtresi.
    """
    q = db.query(BacktestRun)
    if not current_user.is_superuser:
        q = q.filter(
            (BacktestRun.owner_id == current_user.id)
            | (
                BacktestRun.organization_id.isnot(None)
                & (
                    BacktestRun.organization_id
                    == current_user.organization_id
                )
            )
        )
    if preset_id:
        q = q.filter(BacktestRun.preset_id == preset_id)
    if status_filter:
        q = q.filter(BacktestRun.status == status_filter)
    return q.order_by(BacktestRun.created_at.desc()).all()


@router.get(
    "/{run_id}",
    response_model=BacktestResponse,
)
def get_backtest(
    run_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(BacktestRun).filter(BacktestRun.id == run_id)
    if not current_user.is_superuser:
        q = q.filter(
            (BacktestRun.owner_id == current_user.id)
            | (
                BacktestRun.organization_id.isnot(None)
                & (
                    BacktestRun.organization_id
                    == current_user.organization_id
                )
            )
        )
    run = q.first()
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Backtest not found",
        )
    return run


@router.patch(
    "/{run_id}",
    response_model=BacktestResponse,
)
def update_backtest(
    run_id: UUID,
    payload: BacktestUpdate,
    db: Session = Depends(get_db),
):
    """
    Runner / worker burayı kullanarak:
    - status
    - metrics
    - report_ref
    alanlarını günceller.
    UI sonuçları buradan okuyacak.
    """
    run = db.query(BacktestRun).filter(BacktestRun.id == run_id).first()
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Backtest not found",
        )

    if payload.status is not None:
        run.status = payload.status
    if payload.metrics is not None:
        run.metrics = payload.metrics
    if payload.report_ref is not None:
        run.report_ref = payload.report_ref

    db.commit()
    db.refresh(run)
    return run
