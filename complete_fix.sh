#!/bin/bash
# complete_fix.sh - Complete fix for Interview Orchestrator setup

echo "🔧 Complete fix for Interview Orchestrator setup issues..."

# Step 1: Create directory structure
echo "📁 Creating directory structure..."
mkdir -p app/core
mkdir -p app/models
mkdir -p app/schemas
mkdir -p app/api/v1/endpoints
mkdir -p app/services
mkdir -p app/repositories
mkdir -p app/utils
mkdir -p scripts
mkdir -p docker
mkdir -p tests

# Create __init__.py files
touch app/__init__.py
touch app/core/__init__.py
touch app/models/__init__.py
touch app/schemas/__init__.py
touch app/api/__init__.py
touch app/api/v1/__init__.py
touch app/api/v1/endpoints/__init__.py
touch app/services/__init__.py
touch app/repositories/__init__.py
touch app/utils/__init__.py

echo "✅ Directory structure created"

# Step 2: Create .env file (minimal version)
echo "📝 Creating .env file..."
cat > .env << 'EOF'
# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/interview_orchestrator

# JWT Security
SECRET_KEY=your-super-secret-jwt-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Settings
DEBUG=True
LOG_LEVEL=INFO
API_V1_STR=/api/v1
PROJECT_NAME=Interview Orchestrator
VERSION=1.0.0

# CORS Origins (comma-separated)
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:8000
EOF

echo "✅ .env file created"

# Step 3: Create config.py with proper validation
echo "🔧 Creating config.py..."
cat > app/core/config.py << 'EOF'
from pydantic_settings import BaseSettings
from typing import List, Union, Optional
import secrets

class Settings(BaseSettings):
    # Application Settings
    PROJECT_NAME: str = "Interview Orchestrator"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/interview_orchestrator"
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS - Handle both string and list input
    BACKEND_CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # Optional AI Configuration
    OPENAI_API_KEY: Optional[str] = None
    AI_MODEL_PROVIDER: Optional[str] = None
    DEFAULT_AI_MODEL: Optional[str] = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Parse CORS origins if it's a string
        if isinstance(self.BACKEND_CORS_ORIGINS, str):
            if self.BACKEND_CORS_ORIGINS.startswith('['):
                import json
                self.BACKEND_CORS_ORIGINS = json.loads(self.BACKEND_CORS_ORIGINS)
            else:
                self.BACKEND_CORS_ORIGINS = [i.strip() for i in self.BACKEND_CORS_ORIGINS.split(',')]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        # Allow extra fields from environment
        extra = "ignore"

settings = Settings()
EOF

echo "✅ config.py created"

# Step 4: Create database.py
echo "🗄️ Creating database.py..."
cat > app/core/database.py << 'EOF'
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=settings.DEBUG
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
EOF

echo "✅ database.py created"

# Step 5: Create base model
echo "📋 Creating base model..."
cat > app/models/base.py << 'EOF'
from sqlalchemy import Column, DateTime, Integer, Boolean
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime
from app.core.database import Base

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
EOF

echo "✅ base model created"

# Step 6: Create simple user model for testing
echo "👤 Creating user model..."
cat > app/models/user.py << 'EOF'
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
EOF

echo "✅ user model created"

# Step 7: Update models __init__.py
echo "📦 Creating models __init__.py..."
cat > app/models/__init__.py << 'EOF'
from .base import BaseModel
from .user import User

__all__ = [
    "BaseModel",
    "User"
]
EOF

echo "✅ models __init__.py created"

# Step 8: Create simple main.py
echo "🚀 Creating main.py..."
cat > app/main.py << 'EOF'
from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-Powered Interview Orchestrator - Backend Microservice",
)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    }

@app.get("/")
async def root():
    return {"message": "Welcome to Interview Orchestrator API"}
EOF

echo "✅ main.py created"

# Step 9: Create Makefile
echo "📝 Creating Makefile..."
cat > Makefile << 'EOF'
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
EOF

echo "✅ Makefile created"

# Step 10: Test configuration loading
echo "🧪 Testing configuration..."
if uv run python -c "from app.core.config import settings; print('✅ Configuration loads successfully')"; then
    echo "✅ Configuration test passed"
else
    echo "❌ Configuration test failed"
    exit 1
fi

# Step 11: Test FastAPI app
echo "🧪 Testing FastAPI app..."
if uv run python -c "from app.main import app; print('✅ FastAPI app loads successfully')"; then
    echo "✅ FastAPI test passed"
else
    echo "❌ FastAPI test failed"
    exit 1
fi

echo ""
echo "🎉 Complete fix applied successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Update DATABASE_URL in .env with your actual database credentials"
echo "2. Initialize Alembic: make init-alembic"
echo "3. Create initial migration: make create-migration MESSAGE=\"Initial schema\""
echo "4. Run migration: make migrate"
echo "5. Start server: make dev"
echo ""
echo "🔧 Available commands:"
echo "- make help          # Show all available commands"
echo "- make check-config  # Test configuration loading"
echo "- make dev           # Start development server"

echo ""
echo "🌐 Once running, visit:"
echo "- http://localhost:8000 (API root)"
echo "- http://localhost:8000/docs (API documentation)"
echo "- http://localhost:8000/health (Health check)"
EOF
