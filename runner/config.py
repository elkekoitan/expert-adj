"""
MT5 Runner Configuration
"""
from pydantic_settings import BaseSettings
from typing import Optional


class RunnerConfig(BaseSettings):
    """
    Runner servis konfigürasyonu.
    Sadece runner ile ilgili değişkenleri okur.
    Backend (.env) içindeki diğer değişkenleri görmezden gelmek için extra="ignore" kullanılır.
    """

    # API Connection
    API_URL: str = "http://localhost:8000"
    API_KEY: Optional[str] = None
    RUNNER_ID: Optional[str] = None

    # MT Terminal (Tickmill)
    MT5_TERMINAL_PATH: str = r"C:\Program Files (x86)\Tickmill MT4 Client Terminal\terminal.exe"
    MT5_DATA_PATH: Optional[str] = None  # Gerekirse sen dolduracaksın
    MT5_LOGIN: Optional[str] = None
    MT5_PASSWORD: Optional[str] = None
    MT5_SERVER: Optional[str] = None
    MT5_MAX_INSTANCES: int = 1
    MT5_TIMEOUT: int = 3600  # seconds

    # Work Directory
    WORK_DIR: str = "./work"
    EA_DIR: str = "./ea_files"
    RESULTS_DIR: str = "./results"

    # Performance
    MAX_CONCURRENT_TESTS: int = 1
    HEARTBEAT_INTERVAL: int = 30  # seconds

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/runner.log"

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = RunnerConfig()
