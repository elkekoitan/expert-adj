"""
Backtest endpoints
"""
from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def run_backtest():
    """Run backtest"""
    return {"message": "Backtest endpoint - TBD"}


@router.get("/")
async def list_backtests():
    """List all backtests"""
    return {"backtests": [], "total": 0}


@router.get("/{backtest_id}")
async def get_backtest(backtest_id: str):
    """Get backtest details"""
    return {"id": backtest_id, "status": "TBD"}


@router.get("/{backtest_id}/results")
async def get_backtest_results(backtest_id: str):
    """Get backtest results"""
    return {"id": backtest_id, "results": {}}
