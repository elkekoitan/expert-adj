# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Complete project foundation with FastAPI backend
- Next.js 14 frontend with App Router
- Docker Compose development environment
- PostgreSQL + TimescaleDB for data storage
- Redis for caching and task queue
- MinIO for S3-compatible file storage
- Comprehensive database models (User, EA, Optimization, Trading)
- Alembic migrations setup
- MT5 Terminal Controller for backtest automation
- MT5 Runner service
- Genetic Algorithm optimizer
- API endpoints structure (health, auth, EAs, optimization, backtest, trading)

### Documentation
- Comprehensive PRD with market analysis
- Architecture diagrams
- API documentation structure
- Contributing guidelines
- Detailed README with setup instructions

## [0.1.0] - 2025-01-10

### Initial Release
- Project structure and foundation
- Core infrastructure setup
- Development environment ready

---

## Release Notes

### v0.1.0 - Foundation Release

This is the initial release establishing the complete project foundation for MT Expert Optimizer.

**Highlights:**
- ✅ Full-stack application structure
- ✅ Database schema and models
- ✅ MT5 integration layer
- ✅ Docker development environment
- ✅ API endpoints framework
- ✅ Optimization algorithms

**Next Steps:**
- Implement authentication and user management
- Connect API endpoints to database
- Build frontend dashboard UI
- Integrate Celery task queue
- Add real-time WebSocket updates
- Implement backtest result parsing

**Breaking Changes:**
None (initial release)

**Migration Guide:**
```bash
# Setup database
docker-compose up -d postgres redis minio

# Run migrations
cd backend
alembic upgrade head

# Start services
docker-compose up
```

---

For more details, see the [GitHub Releases](https://github.com/yourusername/expert-adj/releases) page.
