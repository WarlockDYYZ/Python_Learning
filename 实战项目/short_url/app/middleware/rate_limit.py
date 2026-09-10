import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.redis import redis_client
from app.core.exceptions import RateLimitExceededException


# Lua 脚本：原子性滑动窗口限流
SLIDING_WINDOW_LUA = """
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local now = tonumber(ARGV[3])-- 清除窗口外的记录
redis.call('ZREMRANGEBYSCORE', key, 0, now - window)-- 当前窗口内的请求数
local count = redis.call('ZCARD', key)
if count < limit then
    -- 
未超限，添加当前请求
    redis.call('ZADD', key, now, now .. '-' .. math.random())
    redis.call('PEXPIRE', key, window)
    return {1, limit - count - 1}
else
    -- 
已超限
    return {0, 0}
end
"""

class RateLimitMiddleware(BaseHTTPMiddleware):
    """滑动窗口限流中间件"""
    def __init__(self, app, limit: int = 100, window: int = 60):
        super().__init__(app)
        self.limit = limit
        self.window = window  # 秒

    async def dispatch(self, request: Request, call_next):
        # 按 IP 限流
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"
        now = int(time.time() * 1000)  # 毫秒

        result = await redis_client.eval(
            SLIDING_WINDOW_LUA, 1, key, self.limit, self.window * 1000, now
        )

        allowed, remaining = int(result[0]), int(result[1])
        if not allowed:
            raise RateLimitExceededException()

        response: Response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response