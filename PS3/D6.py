import time, logging
from functools import wraps
from flask import request, jsonify, g
from app.config import API_KEYS

access_logger = logging.getLogger("access")


def require_api_key(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        key = request.headers.get("X-API-Key", "")
        owner = API_KEYS.get(key)
        if not owner:
            access_logger.warning("DENY path=%s ip=%s", request.path, request.remote_addr)
            return jsonify({"error": "invalid or missing API key"}), 401
        g.api_owner = owner
        return fn(*args, **kwargs)

    return wrapper


def register_access_log(app):
    @app.before_request
    def _start():
        g._t0 = time.time()

    @app.after_request
    def _log(resp):
        cost = (time.time() - getattr(g, "_t0", time.time())) * 1000
        access_logger.info("%s %s -> %s %.1fms owner=%s",
                           request.method, request.path, resp.status_code,
                           cost, getattr(g, "api_owner", "-"))
        return resp