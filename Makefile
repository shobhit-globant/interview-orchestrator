.PHONY: help install dev test clean init-alembic create-migration migrate

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync

dev: ## Start development server
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test: ## Run tests
	uv run pytest

clean: ## Clean cache files
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

init-alembic: ## Initialize Alembic
	uv run alembic init alembic

create-migration: ## Create new migration (usage: make create-migration MESSAGE="description")
ifndef MESSAGE
	$(error MESSAGE is required. Usage: make create-migration MESSAGE="your description")
endif
	uv run alembic revision --autogenerate -m "$(MESSAGE)"

migrate: ## Run database migrations
	uv run alembic upgrade head

check-config: ## Test configuration loading
	uv run python -c "from app.core.config import settings; print('✅ Configuration loads successfully'); print(f'Database URL: {settings.DATABASE_URL}')"
