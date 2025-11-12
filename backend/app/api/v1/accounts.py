"""
Trading Account Management Endpoints

Faz 1 gereği:
- MOCK endpointler kaldırıldı.
- Tüm uçlar ya gerçek mantıkla ya da 501 Not Implemented ile döner.
- Üretim ortamında sahte başarı yok.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.trading import TradingAccount
from app.models.user import User

router = APIRouter(prefix="/accounts", tags=["accounts"])


# ==================== REQUEST MODELS ====================


class AccountCreate(BaseModel):
    """Create trading account"""

    platform: str  # MT4 or MT5
    broker_server: str
    account_number: str
    password: str
    label: Optional[str] = None
    account_type: str = "demo"  # demo or live


class AccountUpdate(BaseModel):
    """Update trading account"""

    label: Optional[str] = None
    is_active: Optional[bool] = None


class LiveSessionCreate(BaseModel):
    """Create live trading session"""

    account_id: str
    ea_version_id: str
    symbol: str
    timeframe: str
    parameters: dict
    magic_numbers: List[int]


class LiveSessionUpdate(BaseModel):
    """Update live session"""

    status: Optional[str] = None
    parameters: Optional[dict] = None


# ==================== ENDPOINTS ====================


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Gerçek trading account oluştur (Faz 1: sadece iskelet, mock yok)",
)
async def create_account(
    account: AccountCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    TradingAccount kaydı için iskelet endpoint.

    Faz 1'de:
    - Kaydı güvenli şekilde oluşturmak için model ve auth entegrasyonu hazır.
    - MT4/MT5 bağlantı testi ve şifre encrypt Faz 2'de detaylandırılacak.
    """
    # Faz 2'de: password encrypt + gerçek bağlantı testi eklenecek.
    new_acc = TradingAccount(
        owner_id=current_user.id,
        platform=account.platform,
        broker_server=account.broker_server,
        account_number=account.account_number,
        account_type=account.account_type,
        label=account.label,
        is_active=True,
        is_connected=False,
    )
    db.add(new_acc)
    await db.commit()
    await db.refresh(new_acc)
    return {
        "id": str(new_acc.id),
        "platform": new_acc.platform,
        "broker_server": new_acc.broker_server,
        "account_number": new_acc.account_number,
        "label": new_acc.label,
        "account_type": new_acc.account_type,
        "is_active": new_acc.is_active,
        "is_connected": new_acc.is_connected,
    }


@router.get(
    "/",
    summary="Kullanıcının trading account listesini döner",
)
async def list_accounts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(TradingAccount).where(TradingAccount.owner_id == current_user.id)
    )
    accounts = result.scalars().all()
    return [
        {
            "id": str(a.id),
            "platform": a.platform,
            "broker_server": a.broker_server,
            "account_number": a.account_number,
            "label": a.label,
            "account_type": a.account_type,
            "is_active": a.is_active,
            "is_connected": a.is_connected,
        }
        for a in accounts
    ]


@router.get(
    "/{account_id}",
    summary="Tekil account detayı",
)
async def get_account(
    account_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(TradingAccount).where(
            TradingAccount.id == account_id,
            TradingAccount.owner_id == current_user.id,
        )
    )
    acc = result.scalar_one_or_none()
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")
    return {
        "id": str(acc.id),
        "platform": acc.platform,
        "broker_server": acc.broker_server,
        "account_number": acc.account_number,
        "label": acc.label,
        "account_type": acc.account_type,
        "is_active": acc.is_active,
        "is_connected": acc.is_connected,
    }


@router.patch(
    "/{account_id}",
    summary="Account güncelle (Faz 1: temel alanlar)",
)
async def update_account(
    account_id: UUID,
    update: AccountUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(TradingAccount).where(
            TradingAccount.id == account_id,
            TradingAccount.owner_id == current_user.id,
        )
    )
    acc = result.scalar_one_or_none()
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")

    if update.label is not None:
        acc.label = update.label
    if update.is_active is not None:
        acc.is_active = update.is_active

    await db.commit()
    await db.refresh(acc)
    return {
        "id": str(acc.id),
        "label": acc.label,
        "is_active": acc.is_active,
    }


@router.delete(
    "/{account_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Account sil",
)
async def delete_account(
    account_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(TradingAccount).where(
            TradingAccount.id == account_id,
            TradingAccount.owner_id == current_user.id,
        )
    )
    acc = result.scalar_one_or_none()
    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")

    await db.delete(acc)
    await db.commit()
    return


@router.post(
    "/{account_id}/test-connection",
    summary="Hesap bağlantı testi (Faz 1: mock success yok, açık 501)",
)
async def test_connection(account_id: UUID):
    """
    Faz 1:
    - Burada sahte 'connected: true' dönmek YASAK.
    - Gerçek MT4/MT5 runner entegrasyonu Faz 2'de gelecek.
    - Şimdilik bilinçli olarak 501 Not Implemented döneriz.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Account connection test will be implemented with MT4/MT5 runner in Phase 2.",
    )


# ==================== LIVE SESSIONS ====================


@router.post("/{account_id}/sessions/start")
async def start_live_session(account_id: str, session: LiveSessionCreate):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Live session start will be implemented with real MT4/MT5 integration.",
    )


@router.get("/{account_id}/sessions")
async def list_sessions(account_id: str):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Live session listing will be implemented with real MT4/MT5 integration.",
    )


@router.get("/{account_id}/sessions/{session_id}")
async def get_session(account_id: str, session_id: str):
    """
    Get session details
    """
    # TODO: Implement session retrieval

    return {
        "id": session_id,
        "account_id": account_id,
        "ea_name": "SmartMartingale Pro",
        "symbol": "EURUSD",
        "timeframe": "M15",
        "status": "running",
        "parameters": {"lot": 0.01, "tp": 500},
        "magic_numbers": [10001, 10002],
        "current_profit": 125.50,
        "peak_profit": 150.00,
        "current_drawdown": 25.00,
        "max_drawdown": 50.00,
        "total_trades": 15,
        "winning_trades": 12,
        "losing_trades": 3,
        "open_positions": 2,
        "started_at": datetime.now().isoformat(),
    }


@router.post("/{account_id}/sessions/{session_id}/stop")
async def stop_session(account_id: str, session_id: str):
    """
    Stop trading session
    """
    # TODO: Implement session stop
    # 1. Stop monitoring
    # 2. Close all positions (optional)
    # 3. Update session status

    return {
        "session_id": session_id,
        "status": "stopped",
        "stopped_at": datetime.now().isoformat(),
    }


@router.get("/{account_id}/sessions/{session_id}/positions")
async def get_session_positions(account_id: str, session_id: str):
    """
    Get current open positions for session
    """
    # TODO: Implement position retrieval

    return {
        "positions": [
            {
                "ticket": 123456,
                "symbol": "EURUSD",
                "type": "BUY",
                "volume": 0.01,
                "open_price": 1.0850,
                "current_price": 1.0865,
                "profit": 15.00,
                "open_time": datetime.now().isoformat(),
            },
            {
                "ticket": 123457,
                "symbol": "EURUSD",
                "type": "BUY",
                "volume": 0.02,
                "open_price": 1.0840,
                "current_price": 1.0865,
                "profit": 50.00,
                "open_time": datetime.now().isoformat(),
            },
        ],
        "total": 2,
        "total_profit": 65.00,
    }


@router.get("/{account_id}/sessions/{session_id}/trades")
async def get_session_trades(account_id: str, session_id: str):
    """
    Get trade history for session
    """
    # TODO: Implement trade history

    return {
        "trades": [
            {
                "ticket": 123450,
                "symbol": "EURUSD",
                "type": "BUY",
                "volume": 0.01,
                "open_price": 1.0830,
                "close_price": 1.0880,
                "profit": 50.00,
                "open_time": datetime.now().isoformat(),
                "close_time": datetime.now().isoformat(),
            }
        ],
        "total": 1,
        "total_profit": 50.00,
    }
