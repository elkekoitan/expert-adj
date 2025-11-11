from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_session
from app.models.strategy import StrategyPreset, BacktestRun

router = APIRouter(prefix="/strategy-presets", tags=["strategy-presets"])


@router.get("/", response_model=List[StrategyPreset])
async def list_presets(session: AsyncSession = Depends(get_session)):
    presets = await StrategyPreset.get_all(session)  # varsayım: model helper mevcut
    return presets


@router.post("/", response_model=StrategyPreset)
async def create_preset(preset_in: StrategyPreset, session: AsyncSession = Depends(get_session)):
    # Not: Gerçek projede ayrı Pydantic şema kullanılır, burada hızlı entegrasyon için model kullanıldı.
    preset = await StrategyPreset.create(session, preset_in)
    return preset


@router.get("/newborn-xauusd", response_model=StrategyPreset)
async def get_newborn_preset(session: AsyncSession = Depends(get_session)):
    """
    NewBornDongu için XAUUSD M15 default preset.
    Yoksa oluşturur, varsa mevcut kaydı döner.
    """
    name = "NewBornDongu_XAUUSD_M15_CORE_v1"
    existing = await StrategyPreset.get_by_name(session, name)
    if existing:
        return existing

    params = {
        "MaxCascadeRobots": 3,
        "TriggerLevel": 3,
        "DistancePercent": 60.0,
        "LotPercent": 100.0,
        "TradeDirection": 2,
        "DailyProfitTarget": 300.0,
    }

    preset = StrategyPreset(
        name=name,
        slug="newborndongu_xauusd_m15_core_v1",
        symbol="XAUUSD",
        timeframe="M15",
        parameters=params,
        description="NewBornDongu XAUUSD M15 core ayar seti"
    )
    preset = await StrategyPreset.create(session, preset)
    return preset


@router.post("/{preset_id}/backtests", response_model=BacktestRun)
async def enqueue_backtest(
    preset_id: int,
    session: AsyncSession = Depends(get_session),
):
    """
    Belirli bir StrategyPreset için BacktestRun kaydı oluşturur.
    Runner şu an çalışıyor ve status=queued kayıtları dinliyor.
    """
    preset = await StrategyPreset.get(session, preset_id)
    if not preset:
        raise HTTPException(status_code=404, detail="Preset not found")

    run = BacktestRun(
        preset_id=preset.id,
        symbol=preset.symbol,
        timeframe=preset.timeframe,
        status="queued",
    )
    run = await BacktestRun.create(session, run)
    return run