# utils/redis_decorator.py
import time
import functools
from Stage_Three.Data_Analysis.Day8.log_config import redis_logger
from opentelemetry import trace

def log_redis_operation(biz_type: str = "default"):
    """
    Redis操作日志记录装饰器，在命令执行前后埋点，记录耗时、链路信息
    :param biz_type: 业务场景标识，如product_cache、order_queue
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 从当前请求的上下文中获取链路ID、请求ID、客户端IP
            request = args[0] if args else None
            trace_id = trace.get_current_span().get_span_context().trace_id
            request_id = getattr(request, "META", {}).get("HTTP_X_REQUEST_ID", "") if request else ""
            client_ip = getattr(request, "META", {}).get("REMOTE_ADDR", "") if request else ""

            # 从Redis命令参数中提取核心命令、Key、用户ID
            redis_command = func.__name__  # 如get、set、hget、rpush
            redis_key = args[1] if len(args) > 1 else kwargs.get("key", "")
            user_id = request.user.id if request and request.user.is_authenticated else ""
            # user_id = request?.user?.id if request?.user?.is_authenticated else ""
            # 记录命令执行前的日志
            redis_logger.info(
                "Redis operation start",
                extra={
                    "trace_id": trace_id,
                    "request_id": request_id,
                    "biz_type": biz_type,
                    "redis_command": redis_command,
                    "redis_key": redis_key,
                    "client_ip": client_ip,
                    "user_id": user_id,
                }
            )

            # 执行实际的Redis命令，计算执行耗时
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                success = True
                error_msg = ""
            except Exception as e:
                result = None
                success = False
                error_msg = str(e)
                # 异常情况下，记录错误级别的日志，包含异常堆栈信息
                redis_logger.error(
                    "Redis operation failed",
                    extra={
                        "trace_id": trace_id,
                        "request_id": request_id,
                        "biz_type": biz_type,
                        "redis_command": redis_command,
                        "redis_key": redis_key,
                        "client_ip": client_ip,
                        "user_id": user_id,
                        "error_msg": error_msg,
                        "cost_time_ms": round((time.time() - start_time) * 1000, 2),
                    },
                    exc_info=True
                )
                raise e
            finally:
                end_time = time.time()
                cost_time = round((end_time - start_time) * 1000, 2)  # 转换为毫秒

            # 记录命令执行成功后的完整日志
            redis_logger.info(
                "Redis operation success",
                extra={
                    "trace_id": trace_id,
                    "request_id": request_id,
                    "biz_type": biz_type,
                    "redis_command": redis_command,
                    "redis_key": redis_key,
                    "client_ip": client_ip,
                    "user_id": user_id,
                    "cost_time_ms": cost_time,
                    "success": success,
                    "result": str(result)[:200] if result else "",  # 截断过长的结果
                }
            )
            return result
        return wrapper
    return decorator