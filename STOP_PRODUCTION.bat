@echo off
REM ============================================================
REM MT EXPERT OPTIMIZER - PRODUCTION STOP SCRIPT
REM ============================================================
REM Stops all services gracefully
REM ============================================================

echo ========================================
echo MT Expert Optimizer - Stop Services
echo ========================================
echo.

docker-compose -f docker-compose.prod.local.yml stop

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to stop services!
    pause
    exit /b 1
)

echo.
echo ========================================
echo All services stopped successfully!
echo ========================================
echo.
echo To start again: START_PRODUCTION.bat
echo To remove completely: docker-compose -f docker-compose.prod.local.yml down
echo.
pause
