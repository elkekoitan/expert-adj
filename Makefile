.PHONY: help
help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Install all dependencies
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

.PHONY: dev
dev: ## Start development environment
	docker-compose up

.PHONY: dev-build
dev-build: ## Build and start development environment
	docker-compose up --build

.PHONY: down
down: ## Stop development environment
	docker-compose down

.PHONY: clean
clean: ## Clean up containers and volumes
	docker-compose down -v
	rm -rf backend/__pycache__
	rm -rf backend/app/__pycache__
	rm -rf frontend/.next
	rm -rf frontend/node_modules

.PHONY: logs
logs: ## Show logs from all services
	docker-compose logs -f

.PHONY: logs-api
logs-api: ## Show API logs
	docker-compose logs -f api

.PHONY: logs-frontend
logs-frontend: ## Show frontend logs
	docker-compose logs -f frontend

.PHONY: db-migrate
db-migrate: ## Run database migrations
	docker-compose exec api alembic upgrade head

.PHONY: db-revision
db-revision: ## Create new migration
	docker-compose exec api alembic revision --autogenerate -m "$(MESSAGE)"

.PHONY: db-downgrade
db-downgrade: ## Downgrade database by 1 revision
	docker-compose exec api alembic downgrade -1

.PHONY: db-shell
db-shell: ## Connect to database shell
	docker-compose exec postgres psql -U postgres -d mt_optimizer

.PHONY: test
test: ## Run all tests
	cd backend && pytest

.PHONY: test-cov
test-cov: ## Run tests with coverage
	cd backend && pytest --cov=app --cov-report=html

.PHONY: lint
lint: ## Run linters
	cd backend && black . && isort . && flake8
	cd frontend && npm run lint

.PHONY: format
format: ## Format code
	cd backend && black . && isort .
	cd frontend && npm run format

.PHONY: shell
shell: ## Open Python shell with app context
	docker-compose exec api python

.PHONY: bash
bash: ## Open bash shell in API container
	docker-compose exec api bash

.PHONY: backup
backup: ## Backup database
	docker-compose exec postgres pg_dump -U postgres mt_optimizer > backup_$$(date +%Y%m%d_%H%M%S).sql

.PHONY: restore
restore: ## Restore database from backup (requires BACKUP_FILE variable)
	docker-compose exec -T postgres psql -U postgres mt_optimizer < $(BACKUP_FILE)

.PHONY: ps
ps: ## Show running containers
	docker-compose ps

.PHONY: restart
restart: ## Restart all services
	docker-compose restart

.PHONY: restart-api
restart-api: ## Restart API service
	docker-compose restart api

.PHONY: restart-frontend
restart-frontend: ## Restart frontend service
	docker-compose restart frontend
