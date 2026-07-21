import logging
from pythonjsonlogger.json import JsonFormatter
import logging.handlers


# 配置JSON日志格式模板，归集核心链路字段
LOG_FORMAT = (
    "%(asctime)s %(levelname)s %(name)s %(message)s "
    "%(trace_id)s %(request_id)s %(biz_type)s "
    "%(redis_command)s %(redis_key)s %(cost_time_ms)s "
    "%(client_ip)s %(server_ip)s"
)

def setup_redis_logger():
    """初始化Redis客户端的日志配置，返回logger实例"""
    logger = logging.getLogger("redis.client")
    logger.setLevel(logging.INFO)
    logger.propagate = False  # 避免日志重复打印

    # 控制台日志输出，开发环境使用
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(JsonFormatter(LOG_FORMAT))
    logger.addHandler(console_handler)

    # 生产环境建议配置FileHandler，按天分割日志
    file_handler = logging.handlers.TimedRotatingFileHandler(
        "/var/logs/redis/redis_client.log",
        when="D",  # 按天分割
        interval=1,  # 间隔天数
        backupCount=30,  # 保留最近30天的日志
        encoding="utf-8"
    )
    file_handler.setFormatter(JsonFormatter(LOG_FORMAT))
    logger.addHandler(file_handler)
    return logger

# 初始化全局Redis日志实例
redis_logger = setup_redis_logger()