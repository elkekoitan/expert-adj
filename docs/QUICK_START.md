# 🚀 Quick Start Guide

Get MT Expert Optimizer up and running in 5 minutes!

## Prerequisites

- Docker and Docker Compose installed
- Git
- 8GB RAM minimum
- (Optional) MT5 Terminal for runner service

## Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/expert-adj.git
cd expert-adj
```

## Step 2: Environment Setup

```bash
cp .env.example .env
# Edit .env if needed (defaults work for development)
```

## Step 3: Start Services

```bash
docker-compose up -d
```

This will start:
- PostgreSQL (port 5432)
- Redis (port 6379)
- MinIO (port 9000, console: 9001)
- FastAPI (port 8000)
- Next.js (port 3000)
- Celery Worker
- Flower (port 5555)

## Step 4: Initialize Database

```bash
# Run migrations
docker-compose exec api alembic upgrade head
```

## Step 5: Access Applications

### Web Interface
Open browser: http://localhost:3000

### API Documentation
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

### MinIO Console
- URL: http://localhost:9001
- Username: `minioadmin`
- Password: `minioadmin`

### Flower (Celery Monitoring)
Open browser: http://localhost:5555

## Step 6: Verify Installation

```bash
# Check all services are running
docker-compose ps

# Check API health
curl http://localhost:8000/health

# Check logs
docker-compose logs -f api
```

## Step 7: Upload Your First EA

### Via Web UI:
1. Go to http://localhost:3000
2. Navigate to EA Library
3. Click "Upload EA"
4. Select your .ex5 or .mq5 file
5. Fill in details and submit

### Via API:
```bash
curl -X POST http://localhost:8000/api/v1/eas/upload \
  -F "file=@/path/to/your/EA.ex5"
```

## Common Tasks

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f frontend
```

### Restart Services
```bash
# All services
docker-compose restart

# Specific service
docker-compose restart api
```

### Stop Everything
```bash
docker-compose down

# With volume cleanup
docker-compose down -v
```

### Database Shell
```bash
docker-compose exec postgres psql -U postgres -d mt_optimizer
```

## Development Workflow

### Backend Development
```bash
# Watch logs
docker-compose logs -f api

# Run migrations
docker-compose exec api alembic upgrade head

# Create new migration
docker-compose exec api alembic revision --autogenerate -m "description"

# Python shell
docker-compose exec api python
```

### Frontend Development
```bash
# Watch logs
docker-compose logs -f frontend

# Install new package
docker-compose exec frontend npm install package-name

# Build
docker-compose exec frontend npm run build
```

### Running Tests
```bash
# Backend tests
docker-compose exec api pytest

# Frontend tests
docker-compose exec frontend npm test
```

## Makefile Shortcuts

We provide a Makefile for common tasks:

```bash
make help           # Show all available commands
make dev            # Start development environment
make down           # Stop environment
make logs           # Show logs
make db-migrate     # Run migrations
make test           # Run tests
make clean          # Clean everything
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port
lsof -i :8000

# Kill process or change port in docker-compose.yml
```

### Database Connection Error
```bash
# Check if postgres is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Restart
docker-compose restart postgres
```

### API Won't Start
```bash
# Check logs for errors
docker-compose logs api

# Rebuild container
docker-compose up --build api
```

### Frontend Build Errors
```bash
# Clean and rebuild
docker-compose exec frontend rm -rf .next node_modules
docker-compose exec frontend npm install
docker-compose restart frontend
```

## Next Steps

1. **Upload EA**: Upload your first Expert Advisor
2. **Configure Optimization**: Set up optimization parameters
3. **Run Backtest**: Execute your first backtest
4. **View Results**: Analyze performance metrics
5. **Deploy to Demo**: Connect demo account and deploy

## Need Help?

- 📖 [Full Documentation](../README.md)
- 🐛 [Report Issues](https://github.com/yourusername/expert-adj/issues)
- 💬 [Discord Community](https://discord.gg/mtoptimizer)
- 📧 [Email Support](mailto:support@mtoptimizer.com)

---

**Happy Trading! 📈**
