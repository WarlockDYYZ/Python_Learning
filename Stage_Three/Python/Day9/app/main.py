from fastapi import FastAPI
from app.api import register_exception_handlers

def create_app() -> FastAPI:
    app = FastAPI(...)
    # 注册全局异常处理器
    register_exception_handlers(app)
    # ... 其余配置
    return app