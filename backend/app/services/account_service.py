"""
Trading Account Service
Handles MT4/MT5 account management and connections
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decrypt_password, encrypt_password
from app.models.trading import TradingAccount
from app.models.user import User

logger = logging.getLogger(__name__)

# MT5 import - optional for Docker
try:
    from runner.mt5.live_connection import MT5LiveConnection

    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False
    MT5LiveConnection = None
    logger.warning("MT5 integration not available - runner module not found")


class AccountService:
    """Trading account service for MT4/MT5 account management"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self._connections: Dict[UUID, Any] = {}  # MT5LiveConnection instances

    async def create_account(
        self,
        user_id: UUID,
        name: str,
        account_type: str,  # demo, live
        broker: str,
        login: int,
        password: str,
        server: str,
        platform: str,  # MT4, MT5
        description: Optional[str] = None,
    ) -> TradingAccount:
        """
        Create a new trading account

        Args:
            user_id: Owner user ID
            name: Account nickname
            account_type: 'demo' or 'live'
            broker: Broker name
            login: MT account login number
            password: MT account password (will be encrypted)
            server: Server name
            platform: MT4 or MT5
            description: Optional description

        Returns:
            Created TradingAccount object
        """
        # Encrypt password before storage
        encrypted_password = encrypt_password(password)

        account = TradingAccount(
            owner_id=user_id,
            label=name,
            account_type=account_type,
            broker_# server field handled above
            account_number=str(login),
            encrypted_password=encrypted_password,
            # server field handled above
            platform=platform,
            description=description,
            is_active=True,
            is_connected=False,
        )

        self.db.add(account)
        await self.db.commit()
        await self.db.refresh(account)

        logger.info(
            f"Created trading account: {account.id} - {account.name} ({account.login})"
        )
        return account

    async def test_connection(self, account_id: UUID) -> Dict[str, Any]:
        """
        Test connection to MT5 account

        Args:
            account_id: Trading account ID

        Returns:
            Connection test result
        """
        # Check if MT5 is available
        if not MT5_AVAILABLE:
            return {
                "success": False,
                "error": "MT5 integration not available in this environment. Please run MT5 runner service separately.",
            }

        account = await self.get_account_by_id(account_id)
        if not account:
            return {"success": False, "error": "Account not found"}

        # Decrypt password
        password = decrypt_password(account.password)

        # Test connection
        conn = MT5LiveConnection()

        try:
            connected = conn.connect(
                login=account.login, password=password, server=account.server
            )

            if connected:
                # Get account info
                account_info = conn.get_account_info()
                conn.disconnect()

                # Update account status
                account.is_connected = True
                account.last_connection = datetime.utcnow()
                await self.db.commit()

                return {
                    "success": True,
                    "message": "Connection successful",
                    "account_info": account_info,
                }
            else:
                return {"success": False, "error": "Failed to connect"}

        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return {"success": False, "error": str(e)}

    async def get_account_by_id(self, account_id: UUID) -> Optional[TradingAccount]:
        """Get account by ID"""
        result = await self.db.execute(
            select(TradingAccount).where(TradingAccount.id == account_id)
        )
        return result.scalar_one_or_none()

    async def list_accounts(
        self,
        user_id: Optional[UUID] = None,
        account_type: Optional[str] = None,
        broker: Optional[str] = None,
        is_active: bool = True,
        limit: int = 50,
        offset: int = 0,
    ) -> List[TradingAccount]:
        """List trading accounts with filters"""
        query = select(TradingAccount).where(TradingAccount.is_active == is_active)

        if user_id:
            query = query.where(TradingAccount.user_id == user_id)

        if account_type:
            query = query.where(TradingAccount.account_type == account_type)

        if broker:
            query = query.where(TradingAccount.broker == broker)

        query = query.limit(limit).offset(offset)

        result = await self.db.execute(query)
        return result.scalars().all()


# Dependency injection
def get_account_service(db: AsyncSession) -> AccountService:
    """FastAPI dependency for account service"""
    return AccountService(db)
