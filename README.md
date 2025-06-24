# AI-Powered Interview Orchestrator

## 🚀 Overview

An intelligent backend microservice for automated candidate screening and evaluation, built with FastAPI and modern Python technologies.

## ✨ Features

- 🤖 AI-powered interview orchestration
- 💻 Secure coding challenge execution
- 📊 Advanced candidate-job matching
- 🏢 Multi-tenant company management
- 📈 Comprehensive analytics and reporting
- 🔒 JWT-based authentication

## 🛠️ Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **Package Manager**: UV
- **Authentication**: JWT
- **Testing**: Pytest

## 🚦 Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL
- UV package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/shobhit-globant/interview-orchestrator.git
   cd interview-orchestrator
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Start the development server**
   ```bash
   uv run uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## 📖 API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🏗️ Project Structure

```
interview-orchestrator/
├── app/
│   ├── api/v1/          # API endpoints
│   ├── core/            # Core configuration
│   ├── models/          # Database models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   ├── repositories/    # Data access
│   ├── utils/           # Utilities
│   └── main.py          # FastAPI app
├── docker/              # Docker config
├── scripts/             # Utility scripts
└── tests/               # Test suite
```

## 🧪 Development

### Code Quality

```bash
# Format code
uv run black app/
uv run isort app/

# Run tests
uv run pytest
```

### Docker

```bash
# Start with Docker Compose
docker-compose -f docker/docker-compose.yml up -d
```

## 📝 License

MIT License - see LICENSE file for details.

---

Made with ❤️ by the Interview Orchestrator Team
