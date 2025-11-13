@echo off
REM ============================================================
REM MT EXPERT OPTIMIZER - VIEW LOGS
REM ============================================================
REM Shows real-time logs from all services
REM Press Ctrl+C to exit
REM ============================================================

echo ========================================
echo MT Expert Optimizer - Live Logs
echo ========================================
echo Press Ctrl+C to exit
echo.

docker-compose -f docker-compose.prod.local.yml logs -f --tail=100
