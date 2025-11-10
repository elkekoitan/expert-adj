"""
MT5 Terminal Controller
Manages MT5 terminal instances for backtesting
"""
import os
import subprocess
import time
import logging
from typing import Dict, Optional, Any
from pathlib import Path
import psutil

logger = logging.getLogger(__name__)


class MT5TerminalController:
    """
    Controls MT5 terminal instances for backtesting
    """

    def __init__(
        self,
        terminal_path: str,
        data_path: str,
        work_dir: str,
        timeout: int = 3600
    ):
        self.terminal_path = terminal_path
        self.data_path = data_path
        self.work_dir = Path(work_dir)
        self.timeout = timeout
        self.process: Optional[subprocess.Popen] = None
        self.instance_id: Optional[str] = None

    def prepare_config(
        self,
        ea_file: str,
        symbol: str,
        timeframe: str,
        date_from: str,
        date_to: str,
        parameters: Dict[str, Any],
        optimization: bool = False,
        deposit: float = 10000,
        leverage: int = 100
    ) -> Path:
        """
        Prepare terminal configuration file

        Args:
            ea_file: Path to EA file
            symbol: Trading symbol
            timeframe: Chart timeframe
            date_from: Start date (YYYY.MM.DD)
            date_to: End date (YYYY.MM.DD)
            parameters: EA parameters dictionary
            optimization: Enable optimization mode
            deposit: Initial deposit
            leverage: Account leverage

        Returns:
            Path to config file
        """
        # Create instance directory
        instance_dir = self.work_dir / f"instance_{time.time()}"
        instance_dir.mkdir(parents=True, exist_ok=True)
        self.instance_id = instance_dir.name

        # Prepare config file
        config_file = instance_dir / "terminal.ini"

        # Convert timeframe to MT5 format
        timeframe_map = {
            "M1": "1",
            "M5": "5",
            "M15": "15",
            "M30": "30",
            "H1": "60",
            "H4": "240",
            "D1": "1440",
            "W1": "10080",
            "MN1": "43200"
        }

        config_content = f"""[Common]
Login=
Password=
Server=

[Tester]
Expert={ea_file}
ExpertParameters={instance_dir / 'parameters.set'}
Symbol={symbol}
Period={timeframe_map.get(timeframe, '60')}
Model=0
ExecutionMode=0
Optimization={1 if optimization else 0}

FromDate={date_from}
ToDate={date_to}

Deposit={deposit}
Currency=USD
Leverage=1:{leverage}

OptimizationCriterion=5

ForwardMode=0
ForwardDate={date_to}

Report={instance_dir / 'report'}
ReplaceReport=1

ShutdownTerminal=1
"""

        config_file.write_text(config_content)

        # Create parameter .set file
        self._create_set_file(instance_dir / "parameters.set", parameters)

        return config_file

    def _create_set_file(self, set_file: Path, parameters: Dict[str, Any]):
        """
        Create .set file from parameters dictionary

        Args:
            set_file: Path to .set file
            parameters: Parameters dictionary
        """
        lines = []
        for key, value in parameters.items():
            # Convert Python types to MQL format
            if isinstance(value, bool):
                value = "true" if value else "false"
            elif isinstance(value, str):
                value = f'"{value}"'

            lines.append(f"{key}={value}")

        set_file.write_text("\n".join(lines))

    def start(self, config_file: Path) -> bool:
        """
        Start MT5 terminal with config

        Args:
            config_file: Path to config file

        Returns:
            True if started successfully
        """
        try:
            cmd = [
                self.terminal_path,
                "/portable",
                f"/config:{config_file.absolute()}"
            ]

            logger.info(f"Starting MT5 terminal: {' '.join(cmd)}")

            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=config_file.parent
            )

            logger.info(f"MT5 terminal started with PID: {self.process.pid}")
            return True

        except Exception as e:
            logger.error(f"Failed to start MT5 terminal: {e}")
            return False

    def wait(self) -> int:
        """
        Wait for terminal to complete

        Returns:
            Exit code
        """
        if not self.process:
            return -1

        try:
            return_code = self.process.wait(timeout=self.timeout)
            logger.info(f"MT5 terminal exited with code: {return_code}")
            return return_code

        except subprocess.TimeoutExpired:
            logger.error(f"MT5 terminal timeout after {self.timeout}s")
            self.kill()
            return -1

    def kill(self):
        """Force kill terminal process"""
        if not self.process:
            return

        try:
            # Kill process tree
            parent = psutil.Process(self.process.pid)
            children = parent.children(recursive=True)

            for child in children:
                child.kill()

            parent.kill()

            logger.info(f"Killed MT5 terminal PID: {self.process.pid}")

        except Exception as e:
            logger.error(f"Failed to kill MT5 terminal: {e}")

    def get_results(self) -> Optional[Dict[str, Any]]:
        """
        Parse backtest results

        Returns:
            Results dictionary or None
        """
        if not self.instance_id:
            return None

        instance_dir = self.work_dir / self.instance_id
        report_html = instance_dir / "report.html"
        report_xml = instance_dir / "report.xml"

        results = {
            "instance_id": self.instance_id,
            "report_html": str(report_html) if report_html.exists() else None,
            "report_xml": str(report_xml) if report_xml.exists() else None,
            "metrics": {}
        }

        # TODO: Parse report files for metrics
        # This would involve parsing HTML or XML to extract:
        # - Net profit
        # - Profit factor
        # - Total trades
        # - Win rate
        # - Drawdown
        # - etc.

        return results

    def cleanup(self):
        """Clean up instance directory"""
        if not self.instance_id:
            return

        instance_dir = self.work_dir / self.instance_id

        try:
            # Keep reports but remove temp files
            for item in instance_dir.glob("*"):
                if not item.name.startswith("report"):
                    if item.is_file():
                        item.unlink()

            logger.info(f"Cleaned up instance: {self.instance_id}")

        except Exception as e:
            logger.error(f"Failed to cleanup instance: {e}")
