from typing import Any, List
from uuid import UUID
import random

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.strategy import StrategyPreset, BacktestRun
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/strategy-presets", tags=["strategy-presets"])


class StrategyPresetOut(BaseModel):
    id: UUID
    name: str
    slug: str
    symbol: str
    timeframe: str
    parameters: dict[str, Any]
    description: str | None = None

    class Config:
        from_attributes = True


@router.get(
    "/",
    response_model=List[StrategyPresetOut],
    summary="Tüm strategy presetleri döner",
)
async def list_presets(db: AsyncSession = Depends(get_db)):
    """
    FE için temel liste endpoint'i.
    Demo slice'ta özellikle NewBorn_XAUUSD_M15_CORE_v1 preset'ini döndürmesi önemli.
    """
    result = await db.execute(select(StrategyPreset))
    return result.scalars().all()


@router.get(
    "/newborn-xauusd",
    response_model=StrategyPresetOut,
    summary="Seedlenmiş NewBorn preset'ini döner (varsa)",
)
async def get_newborn_preset(db: AsyncSession = Depends(get_db)):
    """
    NewBornDongu için XAUUSD M15 default preset.
    Seed script ile oluşturulan slug'a göre arar.
    """
    slug = "newborn_xauusd_m15_core_v1"
    result = await db.execute(
        select(StrategyPreset).where(StrategyPreset.slug == slug)
    )
    existing = result.scalar_one_or_none()
    if not existing:
        raise HTTPException(status_code=404, detail="Preset not found")
    return existing


class BacktestRunOut(BaseModel):
    id: UUID
    preset_id: UUID | None
    symbol: str
    timeframe: str
    date_from: str
    date_to: str
    engine: str
    status: str
    metrics: dict | None = None

    class Config:
        from_attributes = True


@router.post(
    "/{preset_id}/backtests",
    response_model=BacktestRunOut,
    status_code=status.HTTP_201_CREATED,
    summary="Belirli preset için gerçek backtest isteği oluştur (queued)",
)
async def create_backtest_for_preset(
    preset_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Mock YOK.

    Bu endpoint:
    - Seçilen StrategyPreset için BacktestRun kaydını status='queued' olarak oluşturur.
    - Gerçek backtest runner servisi bu kuyruğu okuyup işleyecek.
    - Başarısız durumda sahte başarı dönmez; hata veya queued kayıt döner.
    """
    # Preset kontrolü
    result = await db.execute(
        select(StrategyPreset).where(StrategyPreset.id == preset_id)
    )
    preset = result.scalar_one_or_none()
    if not preset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Preset not found")

    # Temel queued kayıt
    run = BacktestRun(
        owner_id=current_user.id,
        organization_id=current_user.organization_id,
        preset_id=preset.id,
        symbol=preset.symbol or "XAUUSD",
        timeframe=preset.timeframe or "M15",
        # Tarih aralığı ve engine ileride FE veya ayrı API parametresine taşınabilir
        date_from="2020-01-01",
        date_to="2024-01-01",
        engine="mt4_local",
        parameters=preset.parameters or {},
        status="queued",
        metrics=None,
    )
    db.add(run)
    await db.commit()
    await db.refresh(run)
    return run