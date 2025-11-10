"""
Live MT5 Connection Service
Real-time connection to MT5 demo/live accounts
"""
import MetaTrader5 as mt5
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import time

logger = logging.getLogger(__name__)


class MT5LiveConnection:
    """
    Manages live connection to MT5 terminal
    """

    def __init__(self):
        self.connected = False
        self.account_info = None

    def connect(
        self,
        login: int,
        password: str,
        server: str,
        timeout: int = 60000
    ) -> bool:
        """
        Connect to MT5 account

        Args:
            login: Account number
            password: Account password
            server: Broker server
            timeout: Connection timeout (ms)

        Returns:
            True if connected
        """
        try:
            # Initialize MT5
            if not mt5.initialize():
                logger.error(f"MT5 initialize failed: {mt5.last_error()}")
                return False

            # Login to account
            authorized = mt5.login(login=login, password=password, server=server, timeout=timeout)

            if not authorized:
                logger.error(f"MT5 login failed: {mt5.last_error()}")
                mt5.shutdown()
                return False

            self.connected = True
            self.account_info = self.get_account_info()

            logger.info(f"✅ Connected to MT5: {server} - Account: {login}")
            logger.info(f"Balance: ${self.account_info['balance']}, Equity: ${self.account_info['equity']}")

            return True

        except Exception as e:
            logger.error(f"MT5 connection error: {e}")
            return False

    def disconnect(self):
        """Disconnect from MT5"""
        if self.connected:
            mt5.shutdown()
            self.connected = False
            logger.info("Disconnected from MT5")

    def get_account_info(self) -> Optional[Dict[str, Any]]:
        """
        Get account information

        Returns:
            Account info dictionary
        """
        if not self.connected:
            return None

        try:
            account = mt5.account_info()
            if account is None:
                return None

            return {
                "login": account.login,
                "name": account.name,
                "server": account.server,
                "currency": account.currency,
                "balance": account.balance,
                "equity": account.equity,
                "margin": account.margin,
                "free_margin": account.margin_free,
                "margin_level": account.margin_level,
                "profit": account.profit,
                "leverage": account.leverage,
                "trade_allowed": account.trade_allowed,
                "trade_expert": account.trade_expert,
            }

        except Exception as e:
            logger.error(f"Error getting account info: {e}")
            return None

    def get_positions(self, symbol: str = None) -> List[Dict[str, Any]]:
        """
        Get open positions

        Args:
            symbol: Filter by symbol (optional)

        Returns:
            List of positions
        """
        if not self.connected:
            return []

        try:
            if symbol:
                positions = mt5.positions_get(symbol=symbol)
            else:
                positions = mt5.positions_get()

            if positions is None:
                return []

            result = []
            for pos in positions:
                result.append({
                    "ticket": pos.ticket,
                    "time": datetime.fromtimestamp(pos.time),
                    "type": "BUY" if pos.type == 0 else "SELL",
                    "magic": pos.magic,
                    "symbol": pos.symbol,
                    "volume": pos.volume,
                    "price_open": pos.price_open,
                    "sl": pos.sl,
                    "tp": pos.tp,
                    "price_current": pos.price_current,
                    "swap": pos.swap,
                    "profit": pos.profit,
                    "comment": pos.comment,
                })

            return result

        except Exception as e:
            logger.error(f"Error getting positions: {e}")
            return []

    def get_orders(self, symbol: str = None) -> List[Dict[str, Any]]:
        """
        Get pending orders

        Args:
            symbol: Filter by symbol (optional)

        Returns:
            List of orders
        """
        if not self.connected:
            return []

        try:
            if symbol:
                orders = mt5.orders_get(symbol=symbol)
            else:
                orders = mt5.orders_get()

            if orders is None:
                return []

            result = []
            for order in orders:
                result.append({
                    "ticket": order.ticket,
                    "time_setup": datetime.fromtimestamp(order.time_setup),
                    "type": self._order_type_to_string(order.type),
                    "magic": order.magic,
                    "symbol": order.symbol,
                    "volume": order.volume,
                    "price_open": order.price_open,
                    "sl": order.sl,
                    "tp": order.tp,
                    "price_current": order.price_current,
                    "comment": order.comment,
                })

            return result

        except Exception as e:
            logger.error(f"Error getting orders: {e}")
            return []

    def get_history_deals(
        self,
        date_from: datetime,
        date_to: datetime,
        symbol: str = None
    ) -> List[Dict[str, Any]]:
        """
        Get history deals

        Args:
            date_from: Start date
            date_to: End date
            symbol: Filter by symbol (optional)

        Returns:
            List of deals
        """
        if not self.connected:
            return []

        try:
            # Get history
            if symbol:
                deals = mt5.history_deals_get(date_from, date_to, group=symbol)
            else:
                deals = mt5.history_deals_get(date_from, date_to)

            if deals is None:
                return []

            result = []
            for deal in deals:
                result.append({
                    "ticket": deal.ticket,
                    "order": deal.order,
                    "time": datetime.fromtimestamp(deal.time),
                    "type": self._deal_type_to_string(deal.type),
                    "entry": self._deal_entry_to_string(deal.entry),
                    "magic": deal.magic,
                    "symbol": deal.symbol,
                    "volume": deal.volume,
                    "price": deal.price,
                    "commission": deal.commission,
                    "swap": deal.swap,
                    "profit": deal.profit,
                    "comment": deal.comment,
                })

            return result

        except Exception as e:
            logger.error(f"Error getting history: {e}")
            return []

    def place_order(
        self,
        symbol: str,
        order_type: str,
        volume: float,
        price: float = None,
        sl: float = 0,
        tp: float = 0,
        deviation: int = 10,
        magic: int = 0,
        comment: str = ""
    ) -> Optional[Dict[str, Any]]:
        """
        Place order

        Args:
            symbol: Trading symbol
            order_type: BUY or SELL
            volume: Lot size
            price: Price (market if None)
            sl: Stop loss
            tp: Take profit
            deviation: Max price deviation
            magic: Magic number
            comment: Order comment

        Returns:
            Order result
        """
        if not self.connected:
            return None

        try:
            # Prepare request
            symbol_info = mt5.symbol_info(symbol)
            if symbol_info is None:
                logger.error(f"Symbol {symbol} not found")
                return None

            if not symbol_info.visible:
                if not mt5.symbol_select(symbol, True):
                    logger.error(f"Failed to select symbol {symbol}")
                    return None

            # Market order
            if price is None:
                if order_type == "BUY":
                    order_type_mt = mt5.ORDER_TYPE_BUY
                    price = mt5.symbol_info_tick(symbol).ask
                else:
                    order_type_mt = mt5.ORDER_TYPE_SELL
                    price = mt5.symbol_info_tick(symbol).bid
            else:
                # Pending order
                if order_type == "BUY_LIMIT":
                    order_type_mt = mt5.ORDER_TYPE_BUY_LIMIT
                elif order_type == "SELL_LIMIT":
                    order_type_mt = mt5.ORDER_TYPE_SELL_LIMIT
                elif order_type == "BUY_STOP":
                    order_type_mt = mt5.ORDER_TYPE_BUY_STOP
                elif order_type == "SELL_STOP":
                    order_type_mt = mt5.ORDER_TYPE_SELL_STOP
                else:
                    logger.error(f"Invalid order type: {order_type}")
                    return None

            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": volume,
                "type": order_type_mt,
                "price": price,
                "sl": sl,
                "tp": tp,
                "deviation": deviation,
                "magic": magic,
                "comment": comment,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

            # Send order
            result = mt5.order_send(request)

            if result is None:
                logger.error(f"Order send failed: {mt5.last_error()}")
                return None

            if result.retcode != mt5.TRADE_RETCODE_DONE:
                logger.error(f"Order failed: {result.retcode} - {result.comment}")
                return None

            logger.info(f"✅ Order placed: {symbol} {order_type} {volume} @ {price}, Ticket: {result.order}")

            return {
                "retcode": result.retcode,
                "deal": result.deal,
                "order": result.order,
                "volume": result.volume,
                "price": result.price,
                "comment": result.comment,
            }

        except Exception as e:
            logger.error(f"Error placing order: {e}")
            return None

    def close_position(self, ticket: int) -> bool:
        """
        Close position

        Args:
            ticket: Position ticket

        Returns:
            True if closed
        """
        if not self.connected:
            return False

        try:
            positions = mt5.positions_get(ticket=ticket)
            if positions is None or len(positions) == 0:
                logger.error(f"Position {ticket} not found")
                return False

            position = positions[0]

            # Opposite order type
            if position.type == 0:  # BUY
                order_type = mt5.ORDER_TYPE_SELL
                price = mt5.symbol_info_tick(position.symbol).bid
            else:  # SELL
                order_type = mt5.ORDER_TYPE_BUY
                price = mt5.symbol_info_tick(position.symbol).ask

            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": position.symbol,
                "volume": position.volume,
                "type": order_type,
                "position": ticket,
                "price": price,
                "deviation": 10,
                "magic": position.magic,
                "comment": "Close by system",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }

            result = mt5.order_send(request)

            if result is None:
                logger.error(f"Close position failed: {mt5.last_error()}")
                return False

            if result.retcode != mt5.TRADE_RETCODE_DONE:
                logger.error(f"Close failed: {result.retcode} - {result.comment}")
                return False

            logger.info(f"✅ Position closed: {ticket}")
            return True

        except Exception as e:
            logger.error(f"Error closing position: {e}")
            return False

    @staticmethod
    def _order_type_to_string(order_type: int) -> str:
        """Convert order type to string"""
        types = {
            0: "BUY",
            1: "SELL",
            2: "BUY_LIMIT",
            3: "SELL_LIMIT",
            4: "BUY_STOP",
            5: "SELL_STOP",
        }
        return types.get(order_type, "UNKNOWN")

    @staticmethod
    def _deal_type_to_string(deal_type: int) -> str:
        """Convert deal type to string"""
        types = {
            0: "BUY",
            1: "SELL",
            2: "BALANCE",
            3: "CREDIT",
            4: "CHARGE",
            5: "CORRECTION",
            6: "BONUS",
            7: "COMMISSION",
            8: "COMMISSION_DAILY",
            9: "COMMISSION_MONTHLY",
            10: "COMMISSION_AGENT_DAILY",
            11: "COMMISSION_AGENT_MONTHLY",
            12: "INTEREST",
            13: "DEAL_DIVIDEND",
            14: "DEAL_DIVIDEND_FRANKED",
            15: "DEAL_TAX",
        }
        return types.get(deal_type, "UNKNOWN")

    @staticmethod
    def _deal_entry_to_string(entry: int) -> str:
        """Convert deal entry to string"""
        entries = {
            0: "IN",
            1: "OUT",
            2: "INOUT",
            3: "OUT_BY",
        }
        return entries.get(entry, "UNKNOWN")
