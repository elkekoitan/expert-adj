"""
Live Trading Monitor
Monitors live trading sessions and sends updates to API
"""
import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import httpx

from runner.mt5.live_connection import MT5LiveConnection
from runner.config import settings

logger = logging.getLogger(__name__)


class LiveTradingMonitor:
    """
    Monitors active trading sessions
    """

    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
        self.connection = MT5LiveConnection()
        self.running = False
        self.session_id: Optional[str] = None
        self.monitored_magic_numbers: List[int] = []

    async def start_monitoring(
        self,
        session_id: str,
        login: int,
        password: str,
        server: str,
        symbol: str,
        magic_numbers: List[int]
    ):
        """
        Start monitoring a trading session

        Args:
            session_id: Session ID from API
            login: MT5 account login
            password: MT5 account password
            server: Broker server
            symbol: Trading symbol
            magic_numbers: List of magic numbers to monitor
        """
        logger.info(f"Starting live monitoring for session: {session_id}")

        # Connect to MT5
        if not self.connection.connect(login, password, server):
            logger.error("Failed to connect to MT5")
            return False

        self.session_id = session_id
        self.monitored_magic_numbers = magic_numbers
        self.running = True

        # Start monitoring loop
        await self._monitoring_loop()

        return True

    async def stop_monitoring(self):
        """Stop monitoring"""
        self.running = False
        self.connection.disconnect()
        logger.info("Monitoring stopped")

    async def _monitoring_loop(self):
        """Main monitoring loop"""
        last_positions = {}
        last_account_update = None

        while self.running:
            try:
                # Get current positions
                positions = self.connection.get_positions()

                # Filter by magic numbers
                if self.monitored_magic_numbers:
                    positions = [
                        p for p in positions
                        if p['magic'] in self.monitored_magic_numbers
                    ]

                # Check for new/closed positions
                current_tickets = {p['ticket'] for p in positions}
                last_tickets = set(last_positions.keys())

                # New positions
                new_tickets = current_tickets - last_tickets
                for ticket in new_tickets:
                    position = next(p for p in positions if p['ticket'] == ticket)
                    await self._send_position_opened(position)

                # Closed positions
                closed_tickets = last_tickets - current_tickets
                for ticket in closed_tickets:
                    await self._send_position_closed(last_positions[ticket])

                # Update existing positions
                for position in positions:
                    ticket = position['ticket']
                    if ticket in last_positions:
                        # Check if profit changed significantly
                        old_profit = last_positions[ticket]['profit']
                        new_profit = position['profit']

                        if abs(new_profit - old_profit) > 0.01:  # Changed
                            await self._send_position_update(position)

                # Update last positions
                last_positions = {p['ticket']: p for p in positions}

                # Send account update every 5 seconds
                if last_account_update is None or (datetime.now() - last_account_update).seconds >= 5:
                    await self._send_account_update()
                    last_account_update = datetime.now()

                # Wait before next check
                await asyncio.sleep(1)  # Check every second

            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(5)

    async def _send_position_opened(self, position: Dict[str, Any]):
        """Send position opened event"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/api/v1/trading/sessions/{self.session_id}/positions/opened",
                    json=position,
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                response.raise_for_status()

                logger.info(f"✅ Position opened sent: {position['ticket']}")

        except Exception as e:
            logger.error(f"Error sending position opened: {e}")

    async def _send_position_closed(self, position: Dict[str, Any]):
        """Send position closed event"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/api/v1/trading/sessions/{self.session_id}/positions/closed",
                    json=position,
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                response.raise_for_status()

                logger.info(f"✅ Position closed sent: {position['ticket']}")

        except Exception as e:
            logger.error(f"Error sending position closed: {e}")

    async def _send_position_update(self, position: Dict[str, Any]):
        """Send position update"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.patch(
                    f"{self.api_url}/api/v1/trading/sessions/{self.session_id}/positions/{position['ticket']}",
                    json=position,
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                response.raise_for_status()

        except Exception as e:
            logger.error(f"Error sending position update: {e}")

    async def _send_account_update(self):
        """Send account update"""
        try:
            account_info = self.connection.get_account_info()
            if not account_info:
                return

            async with httpx.AsyncClient() as client:
                response = await client.patch(
                    f"{self.api_url}/api/v1/trading/sessions/{self.session_id}/account",
                    json=account_info,
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                response.raise_for_status()

        except Exception as e:
            logger.error(f"Error sending account update: {e}")


# Global monitor instance
_monitor: Optional[LiveTradingMonitor] = None


async def start_live_monitor(
    session_id: str,
    login: int,
    password: str,
    server: str,
    symbol: str,
    magic_numbers: List[int]
) -> bool:
    """
    Start live monitoring

    Args:
        session_id: Session ID
        login: MT5 login
        password: MT5 password
        server: Broker server
        symbol: Trading symbol
        magic_numbers: Magic numbers to monitor

    Returns:
        True if started successfully
    """
    global _monitor

    if _monitor and _monitor.running:
        logger.warning("Monitor already running, stopping...")
        await _monitor.stop_monitoring()

    _monitor = LiveTradingMonitor(
        api_url=settings.API_URL,
        api_key=settings.API_KEY
    )

    return await _monitor.start_monitoring(
        session_id=session_id,
        login=login,
        password=password,
        server=server,
        symbol=symbol,
        magic_numbers=magic_numbers
    )


async def stop_live_monitor():
    """Stop live monitoring"""
    global _monitor

    if _monitor:
        await _monitor.stop_monitoring()
        _monitor = None
