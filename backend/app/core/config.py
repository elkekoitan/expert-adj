"""
Application configuration settings
"""
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, field_validator


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Application
    APP_NAME: str = "MT Expert Optimizer"
    APP_ENV: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_WORKERS: int = 4
    API_RELOAD: bool = True

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    CORS_ALLOW_CREDENTIALS: bool = True

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    # Database
    DATABASE_URL: PostgresDsn
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 0

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_DB: int = 1
    REDIS_CELERY_DB: int = 2

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/2"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    CELERY_TASK_TRACK_STARTED: bool = True
    CELERY_TASK_TIME_LIMIT: int = 7200

    # S3/MinIO
    S3_ENDPOINT: str = "http://localhost:9000"
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "minioadmin"

    # Admin seed (Faz 1+)
    FIRST_SUPERUSER: str | None = None
    FIRST_SUPERUSER_PASSWORD: str | None = None
    S3_BUCKET_NAME: str = "mt-optimizer"
    S3_REGION: str = "us-east-1"
    S3_USE_SSL: bool = False

    # Authentication
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # 2FA
    TOTP_ISSUER: str = "MT Expert Optimizer"
    TOTP_ALGORITHM: str = "SHA1"

    # OAuth (optional)
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GITHUB_CLIENT_ID: Optional[str] = None
    GITHUB_CLIENT_SECRET: Optional[str] = None

    # Email (optional)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM: str = "noreply@mtoptimizer.com"
    SMTP_TLS: bool = True

    # MT5 Runner
    MT5_TERMINAL_PATH: str = "C:\\Program Files\\MetaTrader 5\\terminal64.exe"
    MT5_DATA_PATH: str = "C:\\Users\\User\\AppData\\Roaming\\MetaQuotes\\Terminal"
    MT5_MAX_INSTANCES: int = 5
    MT5_TIMEOUT: int = 3600

    # Optimization
    OPTIMIZATION_MAX_ITERATIONS: int = 1000
    OPTIMIZATION_TIMEOUT: int = 3600
    OPTIMIZATION_PARALLEL_JOBS: int = 4

    # Genetic Algorithm
    GA_POPULATION_SIZE: int = 50
    GA_GENERATIONS: int = 100
    GA_MUTATION_RATE: float = 0.1
    GA_CROSSOVER_RATE: float = 0.8

    # Bayesian Optimization
    BAYESIAN_N_INITIAL_POINTS: int = 10
    BAYESIAN_N_CALLS: int = 100

    # Frontend
    NEXT_PUBLIC_API_URL: str = "http://localhost:8000"
    NEXT_PUBLIC_WS_URL: str = "ws://localhost:8000"

    # Monitoring
    PROMETHEUS_PORT: int = 9090
    GRAFANA_PORT: int = 3001
    SENTRY_DSN: Optional[str] = None
    SENTRY_ENVIRONMENT: str = "development"

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_BURST: int = 100

    # Security
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    SECURE_COOKIES: bool = False
    HTTPS_ONLY: bool = False

    @field_validator("ALLOWED_HOSTS", mode="before")
    @classmethod
    def parse_allowed_hosts(cls, v):
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v

    # Password Policy
    MIN_PASSWORD_LENGTH: int = 8
    REQUIRE_SPECIAL_CHAR: bool = True
    REQUIRE_NUMBER: bool = True
    REQUIRE_UPPERCASE: bool = True

    # File Upload
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    ALLOWED_EA_EXTENSIONS: List[str] = [".ex4", ".ex5", ".mq4", ".mq5"]

    @field_validator("ALLOWED_EA_EXTENSIONS", mode="before")
    @classmethod
    def parse_extensions(cls, v):
        if isinstance(v, str):
            return [ext.strip() for ext in v.split(",")]
        return v


# Create settings instance
settings = Settings()
