"""
MT5 Runner Service
Main entry point for runner service
"""
import asyncio
import logging
import signal
import sys
from pathlib import Path

from runner.config import settings
from runner.mt5.backtest_runner import BacktestRunner

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(settings.LOG_FILE)
    ]
)

logger = logging.getLogger(__name__)


class RunnerService:
    """
    Main runner service
    Polls API for jobs and executes them
    """

    def __init__(self):
        self.backtest_runner = BacktestRunner()
        self.running = True

    async def start(self):
        """Start runner service"""
        logger.info("🚀 Starting MT5 Runner Service")
        logger.info(f"API URL: {settings.API_URL}")
        logger.info(f"MT5 Path: {settings.MT5_TERMINAL_PATH}")
        logger.info(f"Max Concurrent Tests: {settings.MAX_CONCURRENT_TESTS}")

        # Register signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        # Create work directories
        Path(settings.WORK_DIR).mkdir(parents=True, exist_ok=True)
        Path(settings.EA_DIR).mkdir(parents=True, exist_ok=True)
        Path(settings.RESULTS_DIR).mkdir(parents=True, exist_ok=True)
        Path(settings.LOG_FILE).parent.mkdir(parents=True, exist_ok=True)

        # Start main loop
        await self._main_loop()

    async def _main_loop(self):
        """Main event loop"""
        while self.running:
            try:
                # TODO: Poll API for jobs
                # For now, just heartbeat
                logger.info("Runner heartbeat - waiting for jobs...")
                await asyncio.sleep(settings.HEARTBEAT_INTERVAL)

            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                await asyncio.sleep(5)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.running = False

    async def stop(self):
        """Stop runner service"""
        logger.info("👋 Stopping MT5 Runner Service")
        self.running = False


async def main():
    """Main entry point"""
    runner = RunnerService()

    try:
        await runner.start()
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    finally:
        await runner.stop()


if __name__ == "__main__":
    asyncio.run(main())
