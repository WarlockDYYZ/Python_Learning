# app/api/error_handlers.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from loguru import logger
import traceback
import os

from Stage_Three.Python.Day9.app.api.exceptions.base import BusinessException


def register_exception_handlers(app: FastAPI):
    # 1. 业务异常处理器 (捕获 BusinessException 及其子类)
    @app.exception_handler(BusinessException)
    async def business_exception_handler(request: Request, exc: BusinessException):
        logger.error(f"业务异常：{exc.message}，请求地址：{request.url}，详情：{exc.detail}")
        return JSONResponse(
            # 【优化1】使用独立的 http_status 作为 HTTP 响应码，避免非法的 HTTP 状态码
            status_code=exc.http_status,
            content={
                "code": exc.code,  # 业务错误码 (如 40001)
                "message": exc.message,  # 错误描述
                "detail": exc.detail  # 补充信息
            }
        )

    # 2. 参数校验异常处理器 (捕获 Pydantic 校验失败)
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning(f"参数校验失败，请求地址：{request.url}，错误：{exc.errors()}")
        return JSONResponse(
            status_code=422,  # Unprocessable Entity
            content={
                "code": 42200,
                "message": "请求参数校验失败",
                "detail": exc.errors()  # FastAPI 原生的详细错误列表
            }
        )

    # 3. 全局兜底异常处理器 (捕获所有未处理的系统异常)
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        # 记录完整的系统异常堆栈
        logger.error(f"系统异常：{str(exc)}，请求地址：{request.url}\n{traceback.format_exc()}")

        # 【优化2】区分开发与生产环境，防止敏感信息泄露
        is_production = os.getenv("APP_ENV") == "production"
        detail_msg = "系统繁忙，请稍后重试" if is_production else str(exc)

        return JSONResponse(
            status_code=500,
            content={
                "code": 50000,
                "message": "服务器内部错误",
                "detail": detail_msg
            }
        )