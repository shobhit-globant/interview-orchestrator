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
    DATABASE_URL: str = "postgresql://root:postgres@localhost:5432/interview_orchestrator"
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # Optional AI fields
    OPENAI_API_KEY: Optional[str] = None
    AI_MODEL_PROVIDER: Optional[str] = None
    DEFAULT_AI_MODEL: Optional[str] = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Parse CORS origins if it's a string
        if isinstance(self.BACKEND_CORS_ORIGINS, str):
            self.BACKEND_CORS_ORIGINS = [i.strip() for i in self.BACKEND_CORS_ORIGINS.split(',')]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # This allows extra fields

settings = Settings()