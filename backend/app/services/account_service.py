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
from runner.mt5.live_connection import MT5LiveConnection

logger = logging.getLogger(__name__)


class AccountService:
    """Trading account service for MT4/MT5 account management"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self._connections: Dict[UUID, MT5LiveConnection] = {}

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
            user_id=user_id,
            name=name,
            account_type=account_type,
            broker=broker,
            login=login,
            password=encrypted_password,
            server=server,
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

    async def connect_account(self, account_id: UUID) -> bool:
        """
        Establish persistent connection to MT5 account

        Args:
            account_id: Trading account ID

        Returns:
            True if connected
        """
        account = await self.get_account_by_id(account_id)
        if not account:
            return False

        # Check if already connected
        if account_id in self._connections:
            return True

        # Decrypt password
        password = decrypt_password(account.password)

        # Create connection
        conn = MT5LiveConnection()

        try:
            connected = conn.connect(
                login=account.login, password=password, server=account.server
            )

            if connected:
                self._connections[account_id] = conn

                # Update account status
                account.is_connected = True
                account.last_connection = datetime.utcnow()
                await self.db.commit()

                logger.info(f"Connected to account: {account_id}")
                return True
            else:
                return False

        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False

    async def disconnect_account(self, account_id: UUID) -> bool:
        """
        Disconnect from MT5 account

        Args:
            account_id: Trading account ID

        Returns:
            True if disconnected
        """
        if account_id in self._connections:
            conn = self._connections[account_id]
            conn.disconnect()
            del self._connections[account_id]

            # Update account status
            account = await self.get_account_by_id(account_id)
            if account:
                account.is_connected = False
                await self.db.commit()

            logger.info(f"Disconnected from account: {account_id}")
            return True

        return False

    def get_connection(self, account_id: UUID) -> Optional[MT5LiveConnection]:
        """
        Get active MT5 connection

        Args:
            account_id: Trading account ID

        Returns:
            MT5LiveConnection object or None
        """
        return self._connections.get(account_id)

    async def get_account_info(self, account_id: UUID) -> Optional[Dict[str, Any]]:
        """
        Get MT5 account info (balance, equity, etc.)

        Args:
            account_id: Trading account ID

        Returns:
            Account info dict or None
        """
        conn = self.get_connection(account_id)
        if not conn:
            # Try to connect
            connected = await self.connect_account(account_id)
            if not connected:
                return None
            conn = self.get_connection(account_id)

        return conn.get_account_info()

    async def get_positions(
        self, account_id: UUID, symbol: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get open positions

        Args:
            account_id: Trading account ID
            symbol: Optional symbol filter

        Returns:
            List of position dicts
        """
        conn = self.get_connection(account_id)
        if not conn:
            return []

        return conn.get_positions(symbol)

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
        """
        List trading accounts with filters

        Args:
            user_id: Optional user ID filter
            account_type: Optional type filter (demo/live)
            broker: Optional broker filter
            is_active: Filter by active status
            limit: Result limit
            offset: Result offset

        Returns:
            List of TradingAccount objects
        """
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

    async def update_account(
        self,
        account_id: UUID,
        name: Optional[str] = None,
        description: Optional[str] = None,
        password: Optional[str] = None,
    ) -> Optional[TradingAccount]:
        """
        Update account information

        Args:
            account_id: Account ID
            name: Optional new name
            description: Optional new description
            password: Optional new password (will be encrypted)

        Returns:
            Updated TradingAccount or None
        """
        account = await self.get_account_by_id(account_id)
        if not account:
            return None

        if name is not None:
            account.name = name

        if description is not None:
            account.description = description

        if password is not None:
            account.password = encrypt_password(password)
            # Disconnect if connected (password changed)
            await self.disconnect_account(account_id)

        await self.db.commit()
        await self.db.refresh(account)

        return account

    async def delete_account(self, account_id: UUID) -> bool:
        """
        Soft delete account (mark as inactive)

        Args:
            account_id: Account ID

        Returns:
            True if successful
        """
        # Disconnect if connected
        await self.disconnect_account(account_id)

        account = await self.get_account_by_id(account_id)
        if not account:
            return False

        account.is_active = False
        await self.db.commit()

        logger.info(f"Deleted trading account: {account_id}")
        return True

    async def sync_account_data(self, account_id: UUID) -> bool:
        """
        Sync account data from MT5 (balance, equity, etc.)

        Args:
            account_id: Account ID

        Returns:
            True if successful
        """
        account_info = await self.get_account_info(account_id)
        if not account_info:
            return False

        account = await self.get_account_by_id(account_id)
        if not account:
            return False

        # Update account with latest data
        # TODO: Add balance, equity fields to TradingAccount model
        # account.balance = account_info.get('balance')
        # account.equity = account_info.get('equity')
        # account.margin = account_info.get('margin')

        account.last_sync = datetime.utcnow()
        await self.db.commit()

        return True


# Dependency injection
def get_account_service(db: AsyncSession) -> AccountService:
    """FastAPI dependency for account service"""
    return AccountService(db)
