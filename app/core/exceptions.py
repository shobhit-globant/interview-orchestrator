from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError
import logging
from typing import Union
from datetime import datetime

logger = logging.getLogger(__name__)

class InterviewOrchestratorException(Exception):
    """Base exception for Interview Orchestrator"""
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code or "INTERNAL_ERROR"
        super().__init__(self.message)

class NotFoundError(InterviewOrchestratorException):
    def __init__(self, resource: str, identifier: Union[str, int] = None):
        message = f"{resource} not found"
        if identifier:
            message += f" with identifier: {identifier}"
        super().__init__(message, "NOT_FOUND")

class ValidationError(InterviewOrchestratorException):
    def __init__(self, message: str, field: str = None):
        self.field = field
        super().__init__(message, "VALIDATION_ERROR")

class AuthenticationError(InterviewOrchestratorException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, "AUTHENTICATION_ERROR")

class AuthorizationError(InterviewOrchestratorException):
    def __init__(self, message: str = "Access denied"):
        super().__init__(message, "AUTHORIZATION_ERROR")

def create_error_response(
    message: str,
    code: str = "ERROR",
    status_code: int = 500,
    errors: list = None
):
    return JSONResponse(
        status_code=status_code,
        content={
            "data": None,
            "message": message,
            "success": False,
            "timestamp": datetime.utcnow().isoformat(),
            "errors": errors or [],
            "code": code
        }
    )

def setup_exception_handlers(app: FastAPI):
    
    @app.exception_handler(InterviewOrchestratorException)
    async def custom_exception_handler(request: Request, exc: InterviewOrchestratorException):
        logger.error(f"Custom exception: {exc.message}")
        status_map = {
            "NOT_FOUND": 404,
            "VALIDATION_ERROR": 422,
            "AUTHENTICATION_ERROR": 401,
            "AUTHORIZATION_ERROR": 403,
        }
        status_code = status_map.get(exc.code, 500)
        return create_error_response(exc.message, exc.code, status_code)
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.error(f"HTTP exception: {exc.detail}")
        return create_error_response(
            message=exc.detail,
            code="HTTP_ERROR",
            status_code=exc.status_code
        )
    
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        logger.error(f"Validation error: {exc.errors()}")
        errors = [
            {
                "field": error["loc"][-1] if error["loc"] else None,
                "message": error["msg"],
                "code": error["type"]
            }
            for error in exc.errors()
        ]
        return create_error_response(
            message="Validation failed",
            code="VALIDATION_FAILED",
            status_code=422,
            errors=errors
        )
    
    @app.exception_handler(SQLAlchemyError)
    async def database_exception_handler(request: Request, exc: SQLAlchemyError):
        logger.error(f"Database error: {str(exc)}")
        return create_error_response(
            message="Database operation failed",
            code="DATABASE_ERROR",
            status_code=500
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
        return create_error_response(
            message="An unexpected error occurred",
            code="INTERNAL_ERROR",
            status_code=500
        )
