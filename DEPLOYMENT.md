# MT Expert Optimizer - Deployment Guide

Complete guide for deploying the MT Expert Optimizer platform in production or development environments.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start (Development)](#quick-start-development)
3. [Production Deployment](#production-deployment)
4. [Configuration](#configuration)
5. [Database Setup](#database-setup)
6. [Live Trading Setup](#live-trading-setup)
7. [Monitoring & Maintenance](#monitoring--maintenance)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

- **Docker** >= 24.0.0
- **Docker Compose** >= 2.20.0
- **Git** >= 2.30.0

### For Local Development (Optional)

- **Python** 3.11+
- **Node.js** 18+ and npm
- **PostgreSQL** 15+ (if not using Docker)

### Hardware Requirements

**Minimum (Development):**
- 4 GB RAM
- 20 GB disk space
- 2 CPU cores

**Recommended (Production):**
- 16 GB RAM
- 100 GB SSD
- 8 CPU cores
- Dedicated network connection for MT5 integration

---

## Quick Start (Development)

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/expert-adj.git
cd expert-adj
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit configuration (use your preferred editor)
nano .env
```

**Minimal configuration for development:**

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/expert_optimizer

# Security
SECRET_KEY=your-secret-key-minimum-32-characters-long-change-this

# Environment
ENVIRONMENT=development

# API
CORS_ORIGINS=["http://localhost:3000"]
```

### 3. Start All Services

```bash
# Start all services in background
docker compose up -d

# View logs
docker compose logs -f

# Check service status
docker compose ps
```

### 4. Initialize Database

```bash
# Run migrations
docker compose exec api alembic upgrade head

# Verify tables created
docker compose exec postgres psql -U postgres -d expert_optimizer -c "\dt"
```

### 5. Access Services

- **Frontend Dashboard**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API Alternative Docs**: http://localhost:8000/redoc
- **Flower (Celery Monitor)**: http://localhost:5555
- **MinIO Console**: http://localhost:9001 (minioadmin/minioadmin)

### 6. Create First User (Optional)

```bash
docker compose exec api python -c "
from app.core.database import SessionLocal
from app.models import User
from app.core.security import get_password_hash
import uuid

db = SessionLocal()
user = User(
    id=uuid.uuid4(),
    email='admin@example.com',
    hashed_password=get_password_hash('admin123'),
    is_superuser=True,
    is_active=True,
    is_verified=True
)
db.add(user)
db.commit()
print(f'Created user: {user.email}')
"
```

---

## Production Deployment

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### 2. Clone and Configure

```bash
cd /opt
sudo git clone https://github.com/yourusername/expert-adj.git
sudo chown -R $USER:$USER expert-adj
cd expert-adj
```

### 3. Production Environment

Create `.env` with production values:

```env
# Environment
ENVIRONMENT=production
DEBUG=False

# Database (use strong passwords)
DATABASE_URL=postgresql://expertdb_user:CHANGE_THIS_PASSWORD@postgres:5432/expert_optimizer
POSTGRES_DB=expert_optimizer
POSTGRES_USER=expertdb_user
POSTGRES_PASSWORD=CHANGE_THIS_PASSWORD

# Security (generate strong keys)
SECRET_KEY=$(openssl rand -hex 32)
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# API
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=["https://yourdomain.com"]

# Redis
REDIS_URL=redis://redis:6379/0

# MinIO/S3 (use strong credentials)
MINIO_ROOT_USER=CHANGE_THIS
MINIO_ROOT_PASSWORD=CHANGE_THIS_LONG_PASSWORD
AWS_ACCESS_KEY_ID=CHANGE_THIS
AWS_SECRET_ACCESS_KEY=CHANGE_THIS_LONG_PASSWORD
S3_BUCKET=expert-optimizer
S3_ENDPOINT=http://minio:9000

# Celery
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2

# Monitoring
SENTRY_DSN=  # Add if using Sentry

# Email (for notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=noreply@yourdomain.com
```

### 4. SSL/TLS Setup (Nginx Reverse Proxy)

```bash
# Install Nginx
sudo apt install nginx certbot python3-certbot-nginx

# Create Nginx config
sudo nano /etc/nginx/sites-available/expert-optimizer
```

```nginx
upstream api {
    server localhost:8000;
}

upstream frontend {
    server localhost:3000;
}

server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://frontend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /socket.io {
        proxy_pass http://api;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/expert-optimizer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com
```

### 5. Start Production Services

```bash
# Build and start
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Run migrations
docker compose exec api alembic upgrade head

# Check logs
docker compose logs -f api
```

### 6. Setup Systemd Service (Auto-restart)

```bash
sudo nano /etc/systemd/system/expert-optimizer.service
```

```ini
[Unit]
Description=MT Expert Optimizer
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/expert-adj
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable expert-optimizer
sudo systemctl start expert-optimizer
```

---

## Configuration

### Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `ENVIRONMENT` | Environment mode | `development` | Yes |
| `DEBUG` | Enable debug mode | `True` | No |
| `DATABASE_URL` | PostgreSQL connection string | - | Yes |
| `SECRET_KEY` | JWT secret key (min 32 chars) | - | Yes |
| `API_HOST` | API bind address | `0.0.0.0` | No |
| `API_PORT` | API port | `8000` | No |
| `CORS_ORIGINS` | Allowed CORS origins | `["*"]` | Yes |
| `REDIS_URL` | Redis connection string | - | Yes |
| `CELERY_BROKER_URL` | Celery broker URL | - | Yes |
| `S3_ENDPOINT` | MinIO/S3 endpoint | - | Yes |
| `AWS_ACCESS_KEY_ID` | S3 access key | - | Yes |
| `AWS_SECRET_ACCESS_KEY` | S3 secret key | - | Yes |

See `.env.example` for complete list.

---

## Database Setup

### Manual Migration

```bash
# Generate new migration
docker compose exec api alembic revision --autogenerate -m "Description"

# Review migration
cat backend/alembic/versions/XXXXXXX_description.py

# Apply migration
docker compose exec api alembic upgrade head

# Rollback one version
docker compose exec api alembic downgrade -1

# Show current version
docker compose exec api alembic current
```

### Backup Database

```bash
# Create backup
docker compose exec postgres pg_dump -U postgres expert_optimizer > backup_$(date +%Y%m%d).sql

# Restore backup
docker compose exec -T postgres psql -U postgres expert_optimizer < backup_20251110.sql
```

### Database Maintenance

```bash
# Vacuum and analyze
docker compose exec postgres psql -U postgres -d expert_optimizer -c "VACUUM ANALYZE;"

# Check database size
docker compose exec postgres psql -U postgres -d expert_optimizer -c "
  SELECT pg_size_pretty(pg_database_size('expert_optimizer'));"
```

---

## Live Trading Setup

### 1. Add Trading Account

```bash
curl -X POST http://localhost:8000/api/v1/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "MT4",
    "broker_server": "Tickmill-Demo",
    "account_number": "12345678",
    "password": "your_password",
    "account_type": "demo",
    "label": "Tickmill Demo Account"
  }'
```

### 2. Upload EA

```bash
# Upload EA file
curl -X POST http://localhost:8000/api/v1/eas \
  -F "file=@SmartMartingale_Pro_v6.ex4" \
  -F "name=SmartMartingale Pro" \
  -F "platform=MT4" \
  -F "version=6.0"
```

### 3. Start Live Session

```bash
curl -X POST http://localhost:8000/api/v1/accounts/{account_id}/sessions/start \
  -H "Content-Type: application/json" \
  -d '{
    "ea_version_id": "ea-version-uuid",
    "symbol": "EURUSD",
    "timeframe": "M15",
    "parameters": {
      "MaxCascadeRobots": 5,
      "TriggerLevel": 2,
      "Robot1_BuyMagic": 10001,
      "Robot1_SellMagic": 10002
    },
    "magic_numbers": [10001, 10002, 10011, 10012]
  }'
```

### 4. Monitor Dashboard

Open http://localhost:3000/dashboard to view:
- Real-time account balance
- Open positions
- Trade history
- P&L tracking

---

## Monitoring & Maintenance

### Health Checks

```bash
# API health
curl http://localhost:8000/api/v1/health

# Database health
docker compose exec postgres pg_isready

# Redis health
docker compose exec redis redis-cli ping
```

### Logs

```bash
# View all logs
docker compose logs -f

# View specific service
docker compose logs -f api
docker compose logs -f runner
docker compose logs -f celery

# Last 100 lines
docker compose logs --tail=100 api

# Export logs
docker compose logs > logs_$(date +%Y%m%d).txt
```

### Resource Monitoring

```bash
# Docker stats
docker stats

# Disk usage
docker system df

# Clean up unused data
docker system prune -a
```

### Celery Monitoring

Access Flower dashboard:
```
http://localhost:5555
```

Monitor:
- Active tasks
- Task history
- Worker status
- Queue lengths

---

## Troubleshooting

### Services Won't Start

```bash
# Check Docker status
sudo systemctl status docker

# Restart Docker
sudo systemctl restart docker

# Remove old containers
docker compose down -v
docker compose up -d
```

### Database Connection Issues

```bash
# Check PostgreSQL logs
docker compose logs postgres

# Test connection
docker compose exec postgres psql -U postgres -d expert_optimizer -c "SELECT 1;"

# Reset database
docker compose down -v
docker compose up -d postgres
docker compose exec api alembic upgrade head
```

### API Not Responding

```bash
# Check API logs
docker compose logs api

# Restart API
docker compose restart api

# Check if port is in use
sudo netstat -tulpn | grep 8000
```

### MT5 Connection Failed

1. **Check account credentials** in trading_accounts table
2. **Verify broker server** name is correct
3. **Test MetaTrader5 package**:
```python
import MetaTrader5 as mt5
if mt5.initialize():
    print("MT5 OK")
    mt5.shutdown()
```

### WebSocket Disconnects

```bash
# Check Socket.IO logs
docker compose logs api | grep -i socket

# Restart API service
docker compose restart api

# Check firewall rules
sudo ufw status
```

### High Memory Usage

```bash
# Check memory by service
docker stats --no-stream

# Restart heavy services
docker compose restart celery runner

# Increase Docker resources in Docker Desktop settings
```

---

## Backup & Restore

### Complete Backup

```bash
# Backup script
#!/bin/bash
BACKUP_DIR="/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

# Database
docker compose exec postgres pg_dump -U postgres expert_optimizer > $BACKUP_DIR/database.sql

# MinIO data
docker compose exec minio mc mirror local/expert-optimizer $BACKUP_DIR/s3-data/

# Configuration
cp .env $BACKUP_DIR/env.backup

echo "Backup completed: $BACKUP_DIR"
```

### Restore

```bash
# Restore database
docker compose exec -T postgres psql -U postgres expert_optimizer < backup/database.sql

# Restore MinIO
docker compose exec minio mc mirror backup/s3-data/ local/expert-optimizer/
```

---

## Updates & Upgrades

### Update Application

```bash
# Pull latest code
git pull origin main

# Rebuild containers
docker compose build

# Stop services
docker compose down

# Start with new images
docker compose up -d

# Run new migrations
docker compose exec api alembic upgrade head
```

### Update Dependencies

```bash
# Backend
cd backend
pip install -r requirements.txt --upgrade

# Frontend
cd frontend
npm update

# Rebuild
docker compose build --no-cache
```

---

## Security Checklist

- [ ] Change all default passwords
- [ ] Generate strong SECRET_KEY (min 32 characters)
- [ ] Use HTTPS in production (Nginx + Let's Encrypt)
- [ ] Enable firewall (ufw/iptables)
- [ ] Restrict CORS_ORIGINS to your domain
- [ ] Enable rate limiting
- [ ] Set up regular backups
- [ ] Monitor access logs
- [ ] Use strong database passwords
- [ ] Enable 2FA for admin accounts (when implemented)
- [ ] Regularly update Docker images
- [ ] Scan for vulnerabilities (`docker scout`)

---

## Support

- **Documentation**: [README.md](README.md)
- **Live Trading Guide**: [docs/LIVE_TRADING_GUIDE.md](docs/LIVE_TRADING_GUIDE.md)
- **API Documentation**: http://localhost:8000/docs
- **Issues**: https://github.com/yourusername/expert-adj/issues

---

**🎉 You're all set! Happy optimizing!**
