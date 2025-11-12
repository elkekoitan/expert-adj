"""
Backtest endpoints - gerçek enqueue + liste + detay
"""
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.strategy import BacktestRun, StrategyPreset
from app.models.user import User

router = APIRouter(prefix="/backtests", tags=["backtests"])


class BacktestCreate(BaseModel):
    """
    İleriye dönük gerçek runner entegrasyonu için placeholder.
    Bu vertical slice'ta FE direkt /strategy-presets/{id}/backtests kullanacak.
    Buradaki model şimdilik dokunulmadan bırakılıyor.
    """
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


# Not: Bu vertical slice'ta generic POST /backtests kullanmıyoruz.
# FE, doğrudan /strategy-presets/{preset_id}/backtests endpointini çağıracak.


@router.get(
    "/",
    response_model=List[BacktestResponse],
    summary="Kullanıcı backtest listesini döner",
)
async def list_backtests(
    preset_id: Optional[UUID] = None,
    status_filter: Optional[str] = Query(None, alias="status"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Sadece authenticate kullanıcılar:
    - Normal kullanıcı: kendi backtestleri (+ organization paylaşımı ileride)
    - Admin: tüm backtestler
    """
    stmt = select(BacktestRun)

    if not current_user.is_superuser:
        # Basit: sadece kullanıcının kendi kayıtları
        stmt = stmt.where(BacktestRun.owner_id == current_user.id)

    if preset_id:
        stmt = stmt.where(BacktestRun.preset_id == preset_id)
    if status_filter:
        stmt = stmt.where(BacktestRun.status == status_filter)

    stmt = stmt.order_by(BacktestRun.created_at.desc())
    result = await db.execute(stmt)
    runs = result.scalars().all()
    return runs


@router.get(
    "/{run_id}",
    response_model=BacktestResponse,
    summary="Tekil backtest detayı",
)
async def get_backtest(
    run_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = select(BacktestRun).where(BacktestRun.id == run_id)
    if not current_user.is_superuser:
        stmt = stmt.where(BacktestRun.owner_id == current_user.id)

    result = await db.execute(stmt)
    run = result.scalar_one_or_none()
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Backtest not found",
        )
    return run


@router.patch(
    "/{run_id}",
    response_model=BacktestResponse,
    summary="Runner için backtest güncelleme endpointi",
)
async def update_backtest(
    run_id: UUID,
    payload: BacktestUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Gerçek runner entegrasyonu için bırakılıyor.
    Bu vertical slice'ta FE tarafından kullanılmıyor.
    """
    result = await db.execute(
        select(BacktestRun).where(BacktestRun.id == run_id)
    )
    run = result.scalar_one_or_none()
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

    await db.commit()
    await db.refresh(run)
    return run
