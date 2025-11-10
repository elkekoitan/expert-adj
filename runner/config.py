"""
MT5 Runner Configuration
"""
from pydantic_settings import BaseSettings
from typing import Optional


class RunnerConfig(BaseSettings):
    """Runner service configuration"""

    # API Connection
    API_URL: str = "http://localhost:8000"
    API_KEY: Optional[str] = None
    RUNNER_ID: Optional[str] = None

    # MT5 Terminal
    MT5_TERMINAL_PATH: str = "C:\\Program Files\\MetaTrader 5\\terminal64.exe"
    MT5_DATA_PATH: str = "C:\\Users\\User\\AppData\\Roaming\\MetaQuotes\\Terminal"
    MT5_MAX_INSTANCES: int = 5
    MT5_TIMEOUT: int = 3600  # seconds

    # Work Directory
    WORK_DIR: str = "./work"
    EA_DIR: str = "./ea_files"
    RESULTS_DIR: str = "./results"

    # Performance
    MAX_CONCURRENT_TESTS: int = 3
    HEARTBEAT_INTERVAL: int = 30  # seconds

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/runner.log"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = RunnerConfig()
