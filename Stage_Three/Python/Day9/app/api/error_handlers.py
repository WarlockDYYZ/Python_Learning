# app/api/error_handlers.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions.base import BusinessException
from loguru import logger
import traceback

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(BusinessException)
    async def business_exception_handler(request: Request, exc: BusinessException):
        # 记录业务异常日志，包含请求路径、用户信息、异常堆栈
        logger.error(f"业务异常：{exc.message}，请求地址：{request.url}，详情：{exc.detail}")
        return JSONResponse(
            status_code=exc.code,
            content={"code": exc.code, "message": exc.message, "detail": exc.detail}
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        # 记录未捕获的系统异常堆栈
        logger.error(f"系统异常：{str(exc)}，请求地址：{request.url}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={"code": 500, "message": "服务器内部错误", "detail": str(exc)}
        )