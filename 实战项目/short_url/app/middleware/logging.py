import time
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logger import request_id_var, setup_logger


logger = setup_logger()

class LoggingMiddleware(BaseHTTPMiddleware):
    """请求链路追踪中间件"""
    async def dispatch(self, request: Request, call_next):
        # 生成或获取 request_id
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        token = request_id_var.set(request_id)

        start_time = time.time()
        logger.info(
            "请求开始 | method=%s path=%s client=%s",
            request.method, request.url.path, request.client.host
        )

        try:
            response: Response = await call_next(request)
            duration = round((time.time() - start_time) * 1000, 2)
            logger.info(
                "请求完成 | status=%d duration=%.2fms path=%s",
                response.status_code, duration, request.url.path
            )
            response.headers["X-Request-ID"] = request_id
            return response
        except Exception as e:
            duration = round((time.time() - start_time) * 1000, 2)
            logger.exception(
                "请求异常 | duration=%.2fms path=%s error=%s",
                duration, request.url.path, str(e)
            )
            raise
        finally:
            # 清理上下文，防止协程上下文泄漏
            request_id_var.reset(token)