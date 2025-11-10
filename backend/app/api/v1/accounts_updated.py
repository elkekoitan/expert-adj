"""
Trading Account Management Endpoints - Updated with Service Layer
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from app.core.database import get_db
from app.services.account_service import AccountService
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


# ==================== REQUEST MODELS ====================


class AccountCreate(BaseModel):
    """Create trading account"""

    name: str = Field(..., description="Account nickname")
    platform: str = Field(..., description="MT4 or MT5")
    broker: str = Field(..., description="Broker name")
    login: int = Field(..., description="Account login number")
    password: str = Field(..., description="Account password")
    server: str = Field(..., description="Server name (e.g., Tickmill-Demo)")
    account_type: str = Field(default="demo", description="demo or live")
    description: Optional[str] = None


class AccountUpdate(BaseModel):
    """Update trading account"""

    name: Optional[str] = None
    description: Optional[str] = None
    password: Optional[str] = None


# ==================== ENDPOINTS ====================


@router.post("/", status_code=201)
async def create_account(
    account: AccountCreate,
    db: AsyncSession = Depends(get_db),
    # current_user = Depends(get_current_user)  # TODO: Enable
):
    """
    Add trading account (demo/live)

    Request body:
    ```json
    {
        "name": "Tickmill Demo 1",
        "platform": "MT4",
        "broker": "Tickmill",
        "login": 20266961,
        "password": "=a>#qB9RFjzC",
        "server": "Tickmill-Demo",
        "account_type": "demo",
        "description": "Conservative strategy test"
    }
    ```
    """
    account_service = AccountService(db)

    # TODO: Use current_user.id instead of hardcoded UUID
    user_id = uuid4()  # Temporary - replace with current_user.id

    try:
        created_account = await account_service.create_account(
            user_id=user_id,
            name=account.name,
            account_type=account.account_type,
            broker=account.broker,
            login=account.login,
            password=account.password,
            server=account.server,
            platform=account.platform,
            description=account.description,
        )

        return {
            "id": str(created_account.id),
            "name": created_account.name,
            "platform": created_account.platform,
            "broker": created_account.broker,
            "server": created_account.server,
            "login": created_account.login,
            "account_type": created_account.account_type,
            "is_active": created_account.is_active,
            "is_connected": created_account.is_connected,
            "created_at": created_account.created_at.isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
async def list_accounts(
    account_type: Optional[str] = Query(None, description="Filter by type (demo/live)"),
    broker: Optional[str] = Query(None, description="Filter by broker"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """
    List all trading accounts
    """
    account_service = AccountService(db)

    # TODO: Filter by current_user.id
    accounts = await account_service.list_accounts(
        account_type=account_type, broker=broker, limit=limit, offset=offset
    )

    return {
        "accounts": [
            {
                "id": str(acc.id),
                "name": acc.name,
                "platform": acc.platform,
                "broker": acc.broker,
                "server": acc.server,
                "login": acc.login,
                "account_type": acc.account_type,
                "is_active": acc.is_active,
                "is_connected": acc.is_connected,
                "last_connection": acc.last_connection.isoformat()
                if acc.last_connection
                else None,
                "created_at": acc.created_at.isoformat(),
            }
            for acc in accounts
        ],
        "total": len(accounts),
    }


@router.get("/{account_id}")
async def get_account(
    account_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Get account details
    """
    account_service = AccountService(db)
    account = await account_service.get_account_by_id(account_id)

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # Get account info if connected
    account_info = None
    if account.is_connected:
        account_info = await account_service.get_account_info(account_id)

    return {
        "id": str(account.id),
        "name": account.name,
        "platform": account.platform,
        "broker": account.broker,
        "server": account.server,
        "login": account.login,
        "account_type": account.account_type,
        "description": account.description,
        "is_active": account.is_active,
        "is_connected": account.is_connected,
        "last_connection": account.last_connection.isoformat()
        if account.last_connection
        else None,
        "account_info": account_info,
        "created_at": account.created_at.isoformat(),
    }


@router.patch("/{account_id}")
async def update_account(
    account_id: UUID,
    update: AccountUpdate,
    db: AsyncSession = Depends(get_db),
):
    """
    Update account
    """
    account_service = AccountService(db)

    updated_account = await account_service.update_account(
        account_id=account_id,
        name=update.name,
        description=update.description,
        password=update.password,
    )

    if not updated_account:
        raise HTTPException(status_code=404, detail="Account not found")

    return {
        "id": str(updated_account.id),
        "name": updated_account.name,
        "updated": True,
    }


@router.delete("/{account_id}")
async def delete_account(
    account_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete account (soft delete)
    """
    account_service = AccountService(db)
    success = await account_service.delete_account(account_id)

    if not success:
        raise HTTPException(status_code=404, detail="Account not found")

    return {"id": str(account_id), "deleted": True}


@router.post("/{account_id}/test-connection")
async def test_connection(
    account_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Test account connection

    This will:
    1. Retrieve account credentials
    2. Attempt to connect to MT4/MT5
    3. Fetch account info
    4. Disconnect
    5. Return result
    """
    account_service = AccountService(db)
    result = await account_service.test_connection(account_id)

    if not result["success"]:
        raise HTTPException(
            status_code=400, detail=result.get("error", "Connection failed")
        )

    return result


@router.post("/{account_id}/connect")
async def connect_account(
    account_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Establish persistent connection to account
    """
    account_service = AccountService(db)
    success = await account_service.connect_account(account_id)

    if not success:
        raise HTTPException(status_code=400, detail="Failed to connect")

    return {"account_id": str(account_id), "connected": True}


@router.post("/{account_id}/disconnect")
async def disconnect_account(
    account_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Disconnect from account
    """
    account_service = AccountService(db)
    success = await account_service.disconnect_account(account_id)

    return {"account_id": str(account_id), "disconnected": success}


@router.get("/{account_id}/info")
async def get_account_info(
    account_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Get real-time account information from MT5

    Returns:
    - Balance
    - Equity
    - Margin
    - Free margin
    - Profit
    - Leverage
    - Currency
    """
    account_service = AccountService(db)
    account_info = await account_service.get_account_info(account_id)

    if not account_info:
        raise HTTPException(
            status_code=400, detail="Not connected or failed to fetch info"
        )

    return account_info


@router.get("/{account_id}/positions")
async def get_positions(
    account_id: UUID,
    symbol: Optional[str] = Query(None, description="Filter by symbol"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get open positions for account
    """
    account_service = AccountService(db)
    positions = await account_service.get_positions(account_id, symbol)

    return {"positions": positions, "total": len(positions)}
