import logging
import json
from contextvars import ContextVar
from logging.handlers import RotatingFileHandler
from datetime import datetime


# 异步安全的请求 ID 上下文变量
request_id_var: ContextVar[str] = ContextVar("request_id", default="-")

class JsonFormatter(logging.Formatter):
    """JSON 格式日志输出"""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "request_id": request_id_var.get(),
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data, ensure_ascii=False)

    def setup_logger(name: str = "short_link") -> logging.Logger:
        """配置结构化日志"""
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        json_formatter = JsonFormatter()

        # 控制台 Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(json_formatter)
        logger.addHandler(console_handler)

        # 文件 Handler（轮转）
        file_handler = RotatingFileHandler(
            "logs/app.log", maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
        )
        file_handler.setFormatter(json_formatter)
        logger.addHandler(file_handler)

        # 错误文件 Handler（仅 ERROR 及以上）
        error_handler = RotatingFileHandler(
            "logs/error.log", maxBytes=10 * 1024 * 1024, backupCount=3, encoding="utf-8"
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(json_formatter)
        logger.addHandler(error_handler)

        return logger