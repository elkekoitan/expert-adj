"""
Live trading endpoints
"""
from fastapi import APIRouter

router = APIRouter()


@router.post("/accounts")
async def add_account():
    """Add trading account"""
    return {"message": "Add account endpoint - TBD"}


@router.get("/accounts")
async def list_accounts():
    """List trading accounts"""
    return {"accounts": [], "total": 0}


@router.post("/sessions/start")
async def start_trading_session():
    """Start live trading session"""
    return {"message": "Start session endpoint - TBD"}


@router.get("/sessions")
async def list_sessions():
    """List trading sessions"""
    return {"sessions": [], "total": 0}


@router.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Get session details"""
    return {"id": session_id, "status": "TBD"}


@router.post("/sessions/{session_id}/stop")
async def stop_session(session_id: str):
    """Stop trading session"""
    return {"message": f"Session {session_id} stopped"}
