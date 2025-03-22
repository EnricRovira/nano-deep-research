from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, Any

class ErrorType(str, Enum):
    VALIDATION_ERROR = "validation_error"
    AUTHENTICATION_ERROR = "authentication_error"
    AUTHORIZATION_ERROR = "authorization_error"
    RESOURCE_ERROR = "resource_error"
    SERVICE_ERROR = "service_error"
    RATE_LIMIT_ERROR = "rate_limit_error"
    CONTENT_MODERATION_ERROR = "content_moderation_error"
    INTERNAL_ERROR = "internal_error"

class APIError(BaseModel):
    """
    Content of a standard HTTP API error.
    """
    detail: str = Field(
        default="Error description",
        description="Error description"
    )
    error_type: ErrorType = Field(
        default=ErrorType.INTERNAL_ERROR,
        description="Type of error"
    )
    error_code: Optional[str] = Field(
        default=None,
        description="Error code for reference"
    )
    additional_info: Optional[dict[str, Any]] = Field(
        default=None,
        description="Additional information about the error"
    )

class APIException(Exception):
    """Base exception for API errors"""
    def __init__(
        self, 
        detail: str, 
        status_code: int = 500, 
        error_type: ErrorType = ErrorType.INTERNAL_ERROR,
        error_code: Optional[str] = None,
        additional_info: Optional[dict[str, Any]] = None
    ):
        self.detail = detail
        self.status_code = status_code
        self.error_type = error_type
        self.error_code = error_code
        self.additional_info = additional_info
        super().__init__(self.detail)

    def to_api_error(self) -> APIError:
        return APIError(
            detail=self.detail,
            error_type=self.error_type,
            error_code=self.error_code,
            additional_info=self.additional_info
        )

class ValidationError(APIException):
    """Exception for validation errors"""
    def __init__(
        self, 
        detail: str, 
        error_code: Optional[str] = None,
        additional_info: Optional[dict[str, Any]] = None
    ):
        super().__init__(
            detail=detail, 
            status_code=400, 
            error_type=ErrorType.VALIDATION_ERROR,
            error_code=error_code,
            additional_info=additional_info
        )

class AuthenticationError(APIException):
    """Exception for authentication errors"""
    def __init__(
        self, 
        detail: str, 
        error_code: Optional[str] = None,
        additional_info: Optional[dict[str, Any]] = None
    ):
        super().__init__(
            detail=detail, 
            status_code=401, 
            error_type=ErrorType.AUTHENTICATION_ERROR,
            error_code=error_code,
            additional_info=additional_info
        )

class AuthorizationError(APIException):
    """Exception for authorization errors"""
    def __init__(
        self, 
        detail: str, 
        error_code: Optional[str] = None,
        additional_info: Optional[dict[str, Any]] = None
    ):
        super().__init__(
            detail=detail, 
            status_code=403, 
            error_type=ErrorType.AUTHORIZATION_ERROR,
            error_code=error_code,
            additional_info=additional_info
        )

class ResourceError(APIException):
    """Exception for resource errors (not found, etc.)"""
    def __init__(
        self, 
        detail: str, 
        error_code: Optional[str] = None,
        additional_info: Optional[dict[str, Any]] = None
    ):
        super().__init__(
            detail=detail, 
            status_code=404, 
            error_type=ErrorType.RESOURCE_ERROR,
            error_code=error_code,
            additional_info=additional_info
        )

class ContentModerationError(APIException):
    """Exception for content moderation errors"""
    def __init__(
        self, 
        detail: str, 
        error_code: Optional[str] = None,
        additional_info: Optional[dict[str, Any]] = None
    ):
        super().__init__(
            detail=detail, 
            status_code=403, 
            error_type=ErrorType.CONTENT_MODERATION_ERROR,
            error_code=error_code,
            additional_info=additional_info
        )

class ServiceError(APIException):
    """Exception for service errors (external services, etc.)"""
    def __init__(
        self, 
        detail: str, 
        error_code: Optional[str] = None,
        additional_info: Optional[dict[str, Any]] = None
    ):
        super().__init__(
            detail=detail, 
            status_code=503, 
            error_type=ErrorType.SERVICE_ERROR,
            error_code=error_code,
            additional_info=additional_info
        )

class RateLimitError(APIException):
    """Exception for rate limit errors"""
    def __init__(
        self, 
        detail: str, 
        error_code: Optional[str] = None,
        additional_info: Optional[dict[str, Any]] = None
    ):
        super().__init__(
            detail=detail, 
            status_code=429, 
            error_type=ErrorType.RATE_LIMIT_ERROR,
            error_code=error_code,
            additional_info=additional_info
        )