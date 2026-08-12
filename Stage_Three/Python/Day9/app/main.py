from fastapi import FastAPI
from Stage_Three.Python.Day9.app.api.error_handlers import register_exception_handlers

def create_app() -> FastAPI:
    app = FastAPI(...)
    # 注册全局异常处理器
    register_exception_handlers(app)
    # ... 其余配置
    return app