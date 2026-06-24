# app/core/deps.py
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import AsyncSessionLocal


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