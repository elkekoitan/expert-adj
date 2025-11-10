"""
Backtest Runner
Executes backtest jobs from API queue
"""
import logging
import asyncio
from typing import Dict, Any, Optional
from pathlib import Path

from runner.mt5.terminal_controller import MT5TerminalController
from runner.config import settings

logger = logging.getLogger(__name__)


class BacktestRunner:
    """
    Manages backtest execution
    """

    def __init__(self):
        self.work_dir = Path(settings.WORK_DIR)
        self.work_dir.mkdir(parents=True, exist_ok=True)

    async def run_backtest(
        self,
        job_id: str,
        ea_file: str,
        symbol: str,
        timeframe: str,
        date_from: str,
        date_to: str,
        parameters: Dict[str, Any],
        deposit: float = 10000,
        leverage: int = 100
    ) -> Dict[str, Any]:
        """
        Execute single backtest

        Args:
            job_id: Job identifier
            ea_file: Path to EA file
            symbol: Trading symbol
            timeframe: Chart timeframe
            date_from: Start date
            date_to: End date
            parameters: EA parameters
            deposit: Initial deposit
            leverage: Account leverage

        Returns:
            Backtest results
        """
        logger.info(f"Starting backtest job: {job_id}")

        controller = MT5TerminalController(
            terminal_path=settings.MT5_TERMINAL_PATH,
            data_path=settings.MT5_DATA_PATH,
            work_dir=str(self.work_dir),
            timeout=settings.MT5_TIMEOUT
        )

        try:
            # Prepare configuration
            config_file = controller.prepare_config(
                ea_file=ea_file,
                symbol=symbol,
                timeframe=timeframe,
                date_from=date_from,
                date_to=date_to,
                parameters=parameters,
                optimization=False,
                deposit=deposit,
                leverage=leverage
            )

            # Start terminal
            if not controller.start(config_file):
                raise Exception("Failed to start MT5 terminal")

            # Wait for completion
            exit_code = await asyncio.get_event_loop().run_in_executor(
                None,
                controller.wait
            )

            if exit_code != 0:
                raise Exception(f"MT5 terminal exited with code: {exit_code}")

            # Get results
            results = controller.get_results()

            if not results:
                raise Exception("Failed to retrieve results")

            logger.info(f"Backtest job completed: {job_id}")

            return {
                "status": "success",
                "job_id": job_id,
                "results": results
            }

        except Exception as e:
            logger.error(f"Backtest job failed: {job_id} - {e}")

            return {
                "status": "failed",
                "job_id": job_id,
                "error": str(e)
            }

        finally:
            controller.cleanup()

    async def run_optimization(
        self,
        job_id: str,
        ea_file: str,
        symbol: str,
        timeframe: str,
        date_from: str,
        date_to: str,
        parameter_ranges: Dict[str, Dict[str, Any]],
        deposit: float = 10000,
        leverage: int = 100
    ) -> Dict[str, Any]:
        """
        Execute optimization

        Args:
            job_id: Job identifier
            ea_file: Path to EA file
            symbol: Trading symbol
            timeframe: Chart timeframe
            date_from: Start date
            date_to: End date
            parameter_ranges: Parameter ranges for optimization
            deposit: Initial deposit
            leverage: Account leverage

        Returns:
            Optimization results
        """
        logger.info(f"Starting optimization job: {job_id}")

        controller = MT5TerminalController(
            terminal_path=settings.MT5_TERMINAL_PATH,
            data_path=settings.MT5_DATA_PATH,
            work_dir=str(self.work_dir),
            timeout=settings.MT5_TIMEOUT * 10  # Longer timeout for optimization
        )

        try:
            # For MT5 optimization, we use genetic algorithm
            # Parameters are defined in the .set file with Start, Stop, Step

            # TODO: Convert parameter_ranges to .set format
            parameters = {}

            config_file = controller.prepare_config(
                ea_file=ea_file,
                symbol=symbol,
                timeframe=timeframe,
                date_from=date_from,
                date_to=date_to,
                parameters=parameters,
                optimization=True,
                deposit=deposit,
                leverage=leverage
            )

            if not controller.start(config_file):
                raise Exception("Failed to start MT5 terminal")

            exit_code = await asyncio.get_event_loop().run_in_executor(
                None,
                controller.wait
            )

            if exit_code != 0:
                raise Exception(f"MT5 terminal exited with code: {exit_code}")

            results = controller.get_results()

            if not results:
                raise Exception("Failed to retrieve results")

            logger.info(f"Optimization job completed: {job_id}")

            return {
                "status": "success",
                "job_id": job_id,
                "results": results
            }

        except Exception as e:
            logger.error(f"Optimization job failed: {job_id} - {e}")

            return {
                "status": "failed",
                "job_id": job_id,
                "error": str(e)
            }

        finally:
            controller.cleanup()
