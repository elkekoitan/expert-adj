from app.tasks.celery_app import celery_app
from app.core.database import AsyncSessionLocal
from app.models.optimization import BacktestResult, BacktestRun
from sqlalchemy import select
import httpx
import logging
import asyncio

logger = logging.getLogger(__name__)

RUNNER_API_URL = "http://runner:5000"


@celery_app.task(bind=True, name="run_backtest")
def run_backtest_task(self, backtest_run_id: str):
    """
    Execute backtest via runner service
    """
    logger.info(f"Starting backtest task for run_id={backtest_run_id}")
    
    try:
        result = asyncio.run(_execute_backtest(backtest_run_id))
        logger.info(f"Backtest completed for run_id={backtest_run_id}")
        return result
    except Exception as e:
        logger.error(f"Backtest failed for run_id={backtest_run_id}: {str(e)}")
        asyncio.run(_update_backtest_status(backtest_run_id, "failed", str(e)))
        raise


async def _execute_backtest(backtest_run_id: str):
    """
    Execute backtest and update database
    """
    async with AsyncSessionLocal() as db:
        stmt = select(BacktestRun).where(BacktestRun.id == backtest_run_id)
        result = await db.execute(stmt)
        backtest_run = result.scalar_one_or_none()
        
        if not backtest_run:
            raise ValueError(f"BacktestRun {backtest_run_id} not found")
        
        backtest_run.status = "running"
        await db.commit()
    
    async with httpx.AsyncClient(timeout=3600.0) as client:
        response = await client.post(
            f"{RUNNER_API_URL}/backtest",
            json={
                "backtest_run_id": backtest_run_id,
                "ea_version_id": str(backtest_run.ea_version_id),
                "symbol": backtest_run.symbol,
                "timeframe": backtest_run.timeframe,
                "date_from": backtest_run.date_from.isoformat(),
                "date_to": backtest_run.date_to.isoformat(),
                "parameters": backtest_run.parameters,
            },
        )
        response.raise_for_status()
        result_data = response.json()
    
    async with AsyncSessionLocal() as db:
        stmt = select(BacktestRun).where(BacktestRun.id == backtest_run_id)
        result = await db.execute(stmt)
        backtest_run = result.scalar_one_or_none()
        
        if backtest_run:
            backtest_run.status = "completed"
            backtest_run.metrics = result_data.get("metrics", {})
            backtest_run.report_ref = result_data.get("report_ref")
            await db.commit()
    
    return result_data


async def _update_backtest_status(backtest_run_id: str, status: str, error_message: str = None):
    """
    Update backtest status in database
    """
    async with AsyncSessionLocal() as db:
        stmt = select(BacktestRun).where(BacktestRun.id == backtest_run_id)
        result = await db.execute(stmt)
        backtest_run = result.scalar_one_or_none()
        
        if backtest_run:
            backtest_run.status = status
            if error_message:
                backtest_run.error_message = error_message
            await db.commit()


@celery_app.task(bind=True, name="run_optimization")
def run_optimization_task(self, optimization_session_id: str):
    """
    Execute optimization session via runner service
    """
    logger.info(f"Starting optimization task for session_id={optimization_session_id}")
    
    try:
        result = asyncio.run(_execute_optimization(optimization_session_id))
        logger.info(f"Optimization completed for session_id={optimization_session_id}")
        return result
    except Exception as e:
        logger.error(f"Optimization failed for session_id={optimization_session_id}: {str(e)}")
        raise


async def _execute_optimization(optimization_session_id: str):
    """
    Execute optimization and update database
    """
    async with httpx.AsyncClient(timeout=7200.0) as client:
        response = await client.post(
            f"{RUNNER_API_URL}/optimize",
            json={
                "optimization_session_id": optimization_session_id,
            },
        )
        response.raise_for_status()
        result_data = response.json()
    
    return result_data


@celery_app.task(name="cleanup_old_results")
def cleanup_old_results_task():
    """
    Clean up old backtest results (older than 90 days)
    """
    logger.info("Starting cleanup of old backtest results")
    
    try:
        count = asyncio.run(_cleanup_old_results())
        logger.info(f"Cleaned up {count} old backtest results")
        return {"cleaned": count}
    except Exception as e:
        logger.error(f"Cleanup failed: {str(e)}")
        raise


async def _cleanup_old_results():
    """
    Delete old backtest results from database
    """
    from datetime import datetime, timedelta
    
    cutoff_date = datetime.utcnow() - timedelta(days=90)
    
    async with AsyncSessionLocal() as db:
        stmt = select(BacktestResult).where(BacktestResult.created_at < cutoff_date)
        result = await db.execute(stmt)
        old_results = result.scalars().all()
        
        count = len(old_results)
        
        for backtest_result in old_results:
            await db.delete(backtest_result)
        
        await db.commit()
    
    return count
