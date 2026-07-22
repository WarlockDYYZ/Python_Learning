# settings.py
# Redis集群/单实例连接配置，从环境变量中读取，避免硬编码
from utils.redis_logger import LOG_FORMAT

REDIS = {
    "HOST": "redis-cluster.example.com",  # 集群节点地址，单实例则写单机IP
    "PORT": 6379,
    "PASSWORD": "your-redis-password",
    "DB": 0,
    "MAX_CONNECTIONS": 100,  # 连接池最大连接数，根据业务并发规模调整
    "SOCKET_TIMEOUT": 5,  # 套接字读写超时时间，单位秒
    "SOCKET_CONNECT_TIMEOUT": 1,  # 建立连接超时时间，单位秒
    "RETRY_ON_TIMEOUT": True,  # 超时后自动重试
    "decode_responses": True,  # 自动将字节类型结果解码为字符串
    # 集群专属配置，单实例环境删除该配置项
    "CLUSTER": {
        "STARTUP_NODES": [
            {"host": "127.0.0.1", "port": "7001"},
            {"host": "127.0.0.1", "port": "7002"},
            {"host": "127.0.0.1", "port": "7003"}
        ],
        "SKIP_FULL_COVERAGE_CHECK": True,  # 启动时跳过所有节点的覆盖校验
        "RELOAD_ON_FAILURE": True,  # 故障后自动重新加载集群配置
    }
}

# 缓存后端配置，使用Redis作为缓存后端，同时记录操作日志
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://:{REDIS['PASSWORD']}@{REDIS['HOST']}:{REDIS['PORT']}/{REDIS['DB']}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": REDIS["MAX_CONNECTIONS"],
                "socket_timeout": REDIS["SOCKET_TIMEOUT"],
                "socket_connect_timeout": REDIS["SOCKET_CONNECT_TIMEOUT"],
                "retry_on_timeout": REDIS["RETRY_ON_TIMEOUT"],
            },
            "PASSWORD": REDIS["PASSWORD"],
            "DECODE_RESPONSES": REDIS["decode_responses"],
        },
        "KEY_PREFIX": "django_cache",  # 缓存键名前缀，区分不同业务
    }
}

# 日志配置，将Redis操作日志纳入统一日志管理
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": LOG_FORMAT,
        }
    },
    "handlers": {
        "redis_file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "/var/log/redis/django_redis.log",
            "when": "D",
            "interval": 1,
            "backupCount": 30,
            "formatter": "json",
        },
    },
    "loggers": {
        "redis.client": {
            "handlers": ["redis_file"],
            "level": "INFO",
            "propagate": True,
        },
    }
}