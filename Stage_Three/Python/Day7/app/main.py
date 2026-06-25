# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
import httpx


# 定义应用生命周期管理器，绑定资源初始化与清理逻辑
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ======================
    # 应用启动时，初始化全局资源
    # ======================
    # 创建全局异步HTTP客户端，复用连接池
    app.state.http_client = httpx.AsyncClient(
        base_url="https://api.third-service.com/v1",  # 第三方服务基础地址
        timeout=httpx.Timeout(10.0),  # 统一请求超时时间，避免长时间阻塞
        limits=httpx.Limits(
            max_connections=100,  # 连接池最大并发连接数
            max_keepalive_connections=20,  # 保持复用的最大空闲连接数
            keepalive_expiry=3600  # 空闲连接复用超时时间
        ),
        verify=True  # 启用HTTPS证书校验，提升安全性
    )
    print("应用启动：异步HTTP客户端初始化完成，连接池已创建")
    yield
    # ======================
    # 应用关闭时，优雅清理资源
    # ======================
    await app.state.http_client.aclose()
    print("应用关闭：异步HTTP客户端已销毁，连接池资源已释放")

# 初始化FastAPI应用，绑定lifespan生命周期管理器
app = FastAPI(
    title="异步资源复用示例API",
    lifespan=lifespan
)