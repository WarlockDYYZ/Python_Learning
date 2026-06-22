from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from utils.response import fail_response


def register_exception_handlers(app: FastAPI):
    """注册全局异常处理器，统一异常响应格式"""

    # 处理自定义HTTP异常（如主动抛出的404、401）
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return fail_response(
            code=exc.status_code,
            message=exc.detail or "操作失败",
            data=None
        )

    # 处理请求参数校验异常（如422错误）
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        # 格式化校验错误详情，返回给前端具体是哪个字段不符合要求
        error_details = [{"field": err["loc"][-1], "msg": err["msg"]} for err in exc.errors()]
        return fail_response(
            code=422,
            message="请求参数校验失败，请检查输入内容",
            data=error_details
        )

    # 处理全局500服务器异常
    @app.exception_handler(StarletteHTTPException)
    async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
        return fail_response(
            code=exc.status_code,
            message=exc.detail or "操作失败",
            data=None
        )

    # 处理所有未被捕获的未知异常（终极兜底 500 错误）
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        # 建议在这里加上日志记录，方便排查线上 Bug
        # logger.error(f"未捕获的服务器异常: {exc}", exc_info=True)

        return fail_response(
            code=500,
            message="服务器内部错误，请稍后再试",
            data=None
        )