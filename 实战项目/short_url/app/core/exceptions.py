from fastapi import Request
from fastapi.responses import JSONResponse


class AppException(Exception):
    """应用异常基类"""
    def __init__(self, message: str, error_code: str, status_code: int = 400):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(message)

class UrlNotFoundException(AppException):
    def __init__(self, short_code: str):
        super().__init__(
            message=f"短链接 '{short_code}' 不存在",
            error_code="URL_NOT_FOUND",
            status_code=404
        )

class RateLimitExceededException(AppException):
    def __init__(self):
        super().__init__(
            message="请求过于频繁，请稍后再试",
            error_code="RATE_LIMIT_EXCEEDED",
            status_code=429
        )

class ValidationException(AppException):
    def __init__(self, message: str):
        super().__init__(
        message=message,
            error_code="VALIDATION_ERROR",
            status_code=422
        )

async def app_exception_handler(request: Request, exc: AppException):
    """全局异常处理器"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.error_code,
            "message": exc.message
        }
    )