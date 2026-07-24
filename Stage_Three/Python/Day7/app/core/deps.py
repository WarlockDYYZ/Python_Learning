# app/core/deps.py
from typing import AsyncGenerator

import aioredis
from sqlalchemy.ext.asyncio import AsyncSession
from app import AsyncSessionLocal


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    请求级异步数据库会话依赖，通过yield实现上下文管理，保障资源自动回收
    每个请求会获取一个独立会话，事务隔离，请求结束后自动关闭会话并归还连接
    """
    async with AsyncSessionLocal() as session:
        try:
            # 将会话注入路由函数，执行业务逻辑
            yield session
            # 无异常时，自动提交事务
            await session.commit()
        except Exception:
            # 发生异常时，自动回滚事务，避免脏数据残留
            await session.rollback()
            raise
        finally:
            # 关闭会话，将连接归还至连接池，避免连接泄露
            await session.close()


# app/core/deps.py
from fastapi import Request
import httpx

async def get_http_client(request: Request) -> httpx.AsyncClient:
    """
    依赖注入函数：从应用状态中获取全局异步HTTP客户端，复用连接池
    所有请求共享同一个客户端实例，避免频繁创建销毁TCP连接
    """
    return request.app.state.http_client
"""
    关于这段代码的意义
    使用前：
        @app.post("/users")
        async def create_user(user_data: dict):
            async with AsyncSessionLocal() as session:
                try:
                    user = User(**user_data)
                    session.add(user)
                    await session.commit()
                    return {"id": user.id}
                except Exception as e:
                    await session.rollback()
                    raise HTTPException(500, str(e))
    使用后：
        @app.post("/users")
        async def create_user(user_data: dict, db: AsyncSession = Depends(get_session)):
            user = User(**user_data)
            db.add(user)
            # 不需要写 commit，不需要写 rollback，不需要写 try...except
            # 一切由 deps.py 自动接管！
            return {"id": user.id}
"""


# 统一异步资源依赖
from typing import Annotated
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
from app import AsyncSessionLocal


# 1. 数据库会话依赖：请求级，自动管理事务生命周期
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# 2. HTTP客户端依赖：应用级，复用全局连接池
async def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client

# 3. Redis客户端依赖：应用级，复用全局连接池
async def get_redis_client(request: Request) -> aioredis.Redis:
    return request.app.state.redis_client

# 4. 类型别名：统一封装依赖注解，路由中直接复用
AsyncSessionDep = Annotated[AsyncSession, Depends(get_session)]
HttpClientDep = Annotated[httpx.AsyncClient, Depends(get_http_client)]
RedisDep = Annotated[aioredis.Redis, Depends(get_redis_client)]