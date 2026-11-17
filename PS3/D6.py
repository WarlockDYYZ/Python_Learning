import time, hmac, hashlib, uuid, logging
from functools import wraps
from flask import request, jsonify, g
from werkzeug.middleware.proxy_fix import ProxyFix
from app.config import API_KEYS

# 1. 修复日志混淆：为访问日志配置独立的 logger，避免与业务日志混在一起
access_logger = logging.getLogger("access")

# 启动时一次性构建：{sha256(明文key): owner}
_HASHED_KEYS = {
    hashlib.sha256(k.strip().encode("utf-8")).hexdigest(): v
    for k, v in API_KEYS.items()
}


def _get_api_owner(key):
    """解析密钥归属方；未知或空密钥返回 None（默认拒绝）。"""
    if not key:
        return None
    key_hash = hashlib.sha256(key.strip().encode("utf-8")).hexdigest()
    owner = _HASHED_KEYS.get(key_hash)
    if owner is None:
        access_logger.debug("未知 API 密钥摘要: %s...", key_hash[:8])
    return owner


def require_api_key(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        key = request.headers.get("X-API-Key", "")
        owner = _get_api_owner(key)

        if not owner:
            # 4. 修复 IP 伪造漏洞：统一使用 ProxyFix 修正后的 remote_addr，不再读可伪造的原始头
            real_ip = request.remote_addr or "-"
            access_logger.warning("DENY path=%s ip=%s", request.path, real_ip)

            resp = jsonify({"error": "invalid or missing API key"})
            resp.status_code = 401
            resp.headers["WWW-Authenticate"] = "ApiKey"
            return resp

        g.api_owner = owner
        return fn(*args, **kwargs)

    return wrapper


def register_access_log(app):
    # 5. 信任层数需与实际代理跳数一致（Nginx 单层则为 1）
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    @app.before_request
    def _start():
        g._t0 = time.perf_counter()
        g.request_id = uuid.uuid4().hex[:12]
        g._resp_status = None  # 显式初始化，防止 teardown 读取时 AttributeError

    @app.after_request
    def _capture_status(resp):
        g._resp_status = resp.status_code
        resp.headers["X-Request-ID"] = getattr(g, "request_id", "")
        return resp

    @app.teardown_request
    def _log(exception):
        # 3. 修复耗时兜底：_t0 缺失时记为 -1.0ms，避免误导为“极快请求”
        t0 = getattr(g, "_t0", None)
        cost = (time.perf_counter() - t0) * 1000 if t0 is not None else -1.0

        # 1. 修复状态码误判：优先取真实状态码；无响应且无异常时记为 "-"（未知），而非武断的 200
        status = getattr(g, "_resp_status", None)
        if status is None:
            status = 500 if exception else "-"

        req_id = getattr(g, "request_id", "-")
        owner = getattr(g, "api_owner", "-")

        # 2. 修复异常信息丢失：有异常时使用 exception 级别，自动记录完整堆栈和异常对象
        if exception is not None:
            access_logger.exception(
                "rid=%s %s %s -> %s %.1fms owner=%s error=%r",
                req_id, request.method, request.path, status, cost, owner, exception
            )
        else:
            access_logger.info(
                "rid=%s %s %s -> %s %.1fms owner=%s",
                req_id, request.method, request.path, status, cost, owner
            )