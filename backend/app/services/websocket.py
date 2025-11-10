"""
WebSocket Service for Real-time Updates
"""
import socketio
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
    logger=True,
    engineio_logger=True
)


class WebSocketService:
    """
    Manages WebSocket connections and broadcasts
    """

    def __init__(self):
        self.active_connections: Dict[str, List[str]] = {}  # user_id -> [sid, sid, ...]

    async def broadcast_account_update(self, user_id: str, account_id: str, data: Dict[str, Any]):
        """
        Broadcast account update to user

        Args:
            user_id: User ID
            account_id: Account ID
            data: Account data
        """
        await sio.emit(
            'account_update',
            {
                'account_id': account_id,
                'data': data
            },
            room=f'user_{user_id}'
        )

    async def broadcast_position_update(self, user_id: str, session_id: str, positions: List[Dict[str, Any]]):
        """
        Broadcast position updates

        Args:
            user_id: User ID
            session_id: Trading session ID
            positions: List of positions
        """
        await sio.emit(
            'positions_update',
            {
                'session_id': session_id,
                'positions': positions
            },
            room=f'user_{user_id}'
        )

    async def broadcast_trade_opened(self, user_id: str, session_id: str, trade: Dict[str, Any]):
        """
        Broadcast new trade

        Args:
            user_id: User ID
            session_id: Trading session ID
            trade: Trade data
        """
        await sio.emit(
            'trade_opened',
            {
                'session_id': session_id,
                'trade': trade
            },
            room=f'user_{user_id}'
        )

    async def broadcast_trade_closed(self, user_id: str, session_id: str, trade: Dict[str, Any]):
        """
        Broadcast trade closed

        Args:
            user_id: User ID
            session_id: Trading session ID
            trade: Trade data
        """
        await sio.emit(
            'trade_closed',
            {
                'session_id': session_id,
                'trade': trade
            },
            room=f'user_{user_id}'
        )

    async def broadcast_optimization_progress(
        self,
        user_id: str,
        session_id: str,
        progress: int,
        current_best: Dict[str, Any]
    ):
        """
        Broadcast optimization progress

        Args:
            user_id: User ID
            session_id: Optimization session ID
            progress: Progress percentage
            current_best: Current best result
        """
        await sio.emit(
            'optimization_progress',
            {
                'session_id': session_id,
                'progress': progress,
                'current_best': current_best
            },
            room=f'user_{user_id}'
        )


# Global instance
ws_service = WebSocketService()


# Socket.IO event handlers
@sio.event
async def connect(sid, environ):
    """Client connected"""
    logger.info(f"WebSocket client connected: {sid}")


@sio.event
async def disconnect(sid):
    """Client disconnected"""
    logger.info(f"WebSocket client disconnected: {sid}")


@sio.event
async def join_user_room(sid, data):
    """Join user-specific room"""
    user_id = data.get('user_id')
    if user_id:
        await sio.enter_room(sid, f'user_{user_id}')
        logger.info(f"Client {sid} joined room: user_{user_id}")


@sio.event
async def leave_user_room(sid, data):
    """Leave user-specific room"""
    user_id = data.get('user_id')
    if user_id:
        await sio.leave_room(sid, f'user_{user_id}')
        logger.info(f"Client {sid} left room: user_{user_id}")


@sio.event
async def subscribe_session(sid, data):
    """Subscribe to trading session updates"""
    session_id = data.get('session_id')
    if session_id:
        await sio.enter_room(sid, f'session_{session_id}')
        logger.info(f"Client {sid} subscribed to session: {session_id}")


@sio.event
async def unsubscribe_session(sid, data):
    """Unsubscribe from trading session updates"""
    session_id = data.get('session_id')
    if session_id:
        await sio.leave_room(sid, f'session_{session_id}')
        logger.info(f"Client {sid} unsubscribed from session: {session_id}")


# Create ASGI app
socket_app = socketio.ASGIApp(sio, other_asgi_app=None)
