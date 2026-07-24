# 假设在某个操作Redis的函数中
from utils.redis_logger import redis_logger


def get_user_info(user_id):
    # ... 执行Redis命令 ...
    # 记录日志时，通过 extra 参数传入自定义字段
    redis_logger.info(
        "Get user info from Redis",
        extra={
            "trace_id": "abc-123-def-456",
            "request_id": "req-789",
            "biz_type": "user_profile",
            "redis_command": "HGETALL",
            "redis_key": f"user:{user_id}",
            "cost_time_ms": 2.5,
            "client_ip": "192.168.1.100",
            "server_ip": "10.0.0.5"
        }
    )