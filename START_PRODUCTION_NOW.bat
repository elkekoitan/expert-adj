@echo off
cd /d %~dp0
docker-compose -f docker-compose.prod.local.yml --env-file .env.prod up -d
docker-compose -f docker-compose.prod.local.yml ps
pause
