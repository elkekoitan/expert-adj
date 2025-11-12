"""
Demo verisi oluşturma scripti.

Bu script, migration'lara dokunmadan aşağıdaki demo verilerini ekler:
- Admin kullanıcı (admin@example.com / Admin123!)
- Demo kullanıcı (demo@example.com / Demo123!)
- Varsayılan Organization
- NewBornDongu_ParalelRobotlar EA kaydı ve simple EA versiyonu
- NewBorn_XAUUSD_M15_CORE_v1 StrategyPreset
- Bu preset bağlı örnek BacktestRun (status=completed, mock metrikler)

İdempotent tasarlanmıştır: Birden fazla kez çalıştırılabilir.
"""

import asyncio
import os
import sys
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

# backend/ kökünü sys.path'e ekle
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_ROOT = os.path.dirname(CURRENT_DIR)
if BACKEND_ROOT not in sys.path:
    sys.path.insert(0, BACKEND_ROOT)

from app.core.database import AsyncSessionLocal, engine  # type: ignore
from app.core.security import get_password_hash  # type: ignore
from app.models.user import Organization, User  # type: ignore
from app.models.expert_advisor import ExpertAdvisor, EAVersion  # type: ignore
from app.models.strategy import StrategyPreset, BacktestRun  # type: ignore


ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "Admin123!"
DEMO_EMAIL = "demo@example.com"
DEMO_PASSWORD = "Demo123!"


async def get_or_create_default_org(session) -> Organization:
    result = await session.execute(
        select(Organization).where(Organization.slug == "default")
    )
    org = result.scalar_one_or_none()
    if org:
        return org

    org = Organization(name="Default Organization", slug="default", is_active=True)
    session.add(org)
    await session.flush()
    return org


async def get_or_create_user(
    session,
    *,
    email: str,
    password: str,
    is_superuser: bool = False,
    organization: Organization | None = None,
) -> User:
    result = await session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user:
        return user

    username = email.split("@")[0]
    user = User(
        email=email,
        username=username,
        hashed_password=get_password_hash(password),
        is_active=True,
        is_superuser=is_superuser,
        organization_id=organization.id if organization else None,
    )
    session.add(user)
    await session.flush()
    return user


async def get_or_create_newborn_ea(
    session,
    *,
    org: Organization,
    owner: User,
) -> tuple[ExpertAdvisor, EAVersion]:
    """
    Basit bir ExpertAdvisor + EAVersion kaydı oluştur.
    """
    EA_NAME = "NewBornDongu_ParalelRobotlar"

    result = await session.execute(
        select(ExpertAdvisor).where(ExpertAdvisor.name == EA_NAME)
    )
    ea = result.scalar_one_or_none()
    if not ea:
        ea = ExpertAdvisor(
            organization_id=org.id,
            owner_id=owner.id,
            name=EA_NAME,
            description="Demo NewBorn EA - Paralel Robotlar",
            platform="mt4",
            tags=["demo", "newborn", "mt4"],
            is_active=True,
        )
        session.add(ea)
        await session.flush()

    # Basit bir version kaydı (source/compiled path mock)
    result_v = await session.execute(
        select(EAVersion).where(EAVersion.ea_id == ea.id)
    )
    version = result_v.scalar_one_or_none()
    if not version:
        version = EAVersion(
            ea_id=ea.id,
            version="1.0.0",
            compiled_file_path="examples/EAs/NewBornDongu_ParalelRobotlar.ex4",
            source_file_path="examples/EAs/NewBornDongu_ParalelRobotlar.mq4",
            source_present=True,
            requires_sdk=False,
            compiled_at=datetime.utcnow().isoformat(),
            meta_data={"note": "demo version"},
        )
        session.add(version)
        await session.flush()

    return ea, version


async def get_or_create_newborn_preset(
    session,
    *,
    ea: ExpertAdvisor,
    owner: User,
    org: Organization,
) -> StrategyPreset:
    """
    NewBorn_XAUUSD_M15_CORE_v1 presetini oluşturur.
    """
    slug = "newborn_xauusd_m15_core_v1"

    result = await session.execute(
        select(StrategyPreset).where(StrategyPreset.slug == slug)
    )
    preset = result.scalar_one_or_none()
    if preset:
        return preset

    parameters = {
        "Symbol": "XAUUSD",
        "Timeframe": "M15",
        "InitialDeposit": 10000,
        "MaxCascadeRobots": 5,
        "TriggerLevel": 2.0,
        "BaseLot": 0.1,
        "TakeProfitPoints": 500,
        "StopLossPoints": 300,
        "MagicNumber": 20251111,
        "RiskMode": "fixed",
    }

    preset = StrategyPreset(
        owner_id=owner.id,
        organization_id=org.id,
        ea_id=ea.id,
        name="NewBorn_XAUUSD_M15_CORE_v1",
        slug=slug,
        description="NewBornDongu için XAUUSD M15 core demo strateji",
        symbol="XAUUSD",
        timeframe="M15",
        mode="manual",
        parameters=parameters,
        status="tested",
        tags=["demo", "newborn", "xauusd", "m15"],
        metrics_snapshot={
            "net_profit": 1520.35,
            "max_drawdown": 4.2,
            "total_trades": 124,
            "profit_factor": 1.85,
        },
    )
    session.add(preset)
    await session.flush()
    return preset


async def ensure_mock_backtest(
    session,
    *,
    org: Organization,
    owner: User,
    preset: StrategyPreset,
):
    """
    Presete bağlı en az bir completed BacktestRun oluştur.
    """
    result = await session.execute(
        select(BacktestRun).where(
            BacktestRun.preset_id == preset.id,
            BacktestRun.status == "completed",
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        return existing

    run = BacktestRun(
        owner_id=owner.id,
        organization_id=org.id,
        preset_id=preset.id,
        symbol=preset.symbol or "XAUUSD",
        timeframe=preset.timeframe or "M15",
        date_from="2020-01-01",
        date_to="2024-01-01",
        engine="mt4_local",
        parameters=preset.parameters,
        status="completed",
        metrics={
            "net_profit": 1500.0,
            "max_drawdown": 3.8,
            "total_trades": 120,
            "win_rate": 0.62,
            "profit_factor": 1.8,
        },
        report_ref="demo/newborn_xauusd_m15_core_v1_report.html",
    )
    session.add(run)
    await session.flush()
    return run


async def init_demo_data():
    print("🚀 Demo verisi inizyalizasyonu başlıyor...")

    # Tablo varlığı bekleniyor; migration'lar önceden çalıştırılmış olmalı.
    async with AsyncSessionLocal() as session:
        try:
            org = await get_or_create_default_org(session)

            admin = await get_or_create_user(
                session,
                email=ADMIN_EMAIL,
                password=ADMIN_PASSWORD,
                is_superuser=True,
                organization=org,
            )

            demo_user = await get_or_create_user(
                session,
                email=DEMO_EMAIL,
                password=DEMO_PASSWORD,
                is_superuser=False,
                organization=org,
            )

            ea, ea_version = await get_or_create_newborn_ea(
                session, org=org, owner=admin
            )

            preset = await get_or_create_newborn_preset(
                session, ea=ea, owner=admin, org=org
            )

            await ensure_mock_backtest(
                session, org=org, owner=admin, preset=preset
            )

            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            print(f"⚠️ IntegrityError: {e}")
        except Exception as e:
            await session.rollback()
            print(f"❌ Hata: {e}")
            raise

    print("✅ Demo verisi hazır.")
    print(f"- Admin: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")
    print(f"- Demo:  {DEMO_EMAIL} / {DEMO_PASSWORD}")


def main():
    asyncio.run(init_demo_data())


if __name__ == "__main__":
    main()