@echo off
REM ============================================================
REM MT EXPERT OPTIMIZER - PRODUCTION STARTUP SCRIPT
REM ============================================================
REM Quick start script for Windows
REM ============================================================

echo ========================================
echo MT Expert Optimizer - Production Start
echo ========================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo [OK] Docker is running
echo.

REM Check if .env.prod exists
if not exist .env.prod (
    echo [ERROR] .env.prod file not found!
    echo Please create .env.prod file first.
    pause
    exit /b 1
)

echo [OK] Environment file found
echo.

REM Start services
echo Starting MT Optimizer services...
echo This may take 2-5 minutes on first run...
echo.

docker-compose -f docker-compose.prod.local.yml --env-file .env.prod up -d --build

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to start services!
    echo Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Services started successfully!
echo ========================================
echo.
echo Web Interfaces:
echo   - Frontend:       http://localhost
echo   - API Docs:       http://localhost/api/docs
echo   - Flower:         http://localhost/flower/
echo   - Grafana:        http://localhost/grafana/
echo   - MinIO Console:  http://localhost:9001
echo.
echo Login Credentials:
echo   - Frontend:  admin@mtoptimizer.local / Admin2025!SuperSecure#Pass
echo   - Flower:    admin / Admin2025
echo   - Grafana:   admin / Grafana2025!Admin#Pass
echo   - MinIO:     minioadmin / MinIO2025!StorageSecure#Pass
echo.
echo Waiting for services to be ready (30 seconds)...
timeout /t 30 /nobreak >nul

echo.
echo Opening frontend in browser...
start http://localhost

echo.
echo To view logs: docker-compose -f docker-compose.prod.local.yml logs -f
echo To stop:      docker-compose -f docker-compose.prod.local.yml stop
echo.
pause
