from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager, asynccontextmanager
from typing import Dict
import logging

logger = logging.getLogger(__name__)

# 全局连接池字典，以数据源名称为 Key
sync_pools: Dict[str, sessionmaker] = {}
async_pools: Dict[str, sessionmaker] = {}

# 保存引擎实例，用于优雅退出时释放连接
sync_engines = {}
async_engines = {}


def init_sync_pool(source_name: str, db_url: str, pool_size: int = 10, max_overflow: int = 20):
    """初始化同步数据库连接池"""
    engine = create_engine(
        db_url,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_pre_ping=True,  # 每次获取连接前检测有效性，防止断连报错
        echo=False
    )
    sync_engines[source_name] = engine
    sync_pools[source_name] = sessionmaker(bind=engine, class_=Session)
    logger.info(f"同步连接池 [{source_name}] 初始化成功")


def init_async_pool(source_name: str, db_url: str, pool_size: int = 10, max_overflow: int = 20):
    """初始化异步数据库连接池"""
    engine = create_async_engine(
        db_url,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_pre_ping=True,
        echo=False
    )
    async_engines[source_name] = engine
    async_pools[source_name] = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    logger.info(f"异步连接池 [{source_name}] 初始化成功")


# 上下文管理器封装

@contextmanager
def get_sync_session_ctx(source_name: str):
    """
    同步会话上下文管理器
    自动处理：事务提交、异常回滚、连接归还
    """
    if source_name not in sync_pools:
        raise ValueError(f"未找到同步数据源: {source_name}")

    session = sync_pools[source_name]()
    try:
        yield session
        session.commit()  # 正常执行完毕，自动提交事务
    except Exception as e:
        session.rollback()  # 发生异常，自动回滚事务
        logger.error(f"同步会话执行异常并已回滚: {str(e)}")
        raise
    finally:
        session.close()  # 无论成功失败，必须关闭会话，归还连接到连接池


@asynccontextmanager
async def get_async_session_ctx(source_name: str):
    """
    异步会话上下文管理器
    自动处理：事务提交、异常回滚、连接归还
    """
    if source_name not in async_pools:
        raise ValueError(f"未找到异步数据源: {source_name}")

    session = async_pools[source_name]()
    try:
        yield session
        await session.commit()  # 异步自动提交
    except Exception as e:
        await session.rollback()  # 异步自动回滚
        logger.error(f"异步会话执行异常并已回滚: {str(e)}")
        raise
    finally:
        await session.close()  # 异步关闭会话


# 生命周期管理

async def close_all_pools():
    """
    优雅关闭所有连接池（在应用退出或热重载时调用）
    释放底层数据库连接，防止资源泄漏
    """
    for name, engine in sync_engines.items():
        engine.dispose()
        logger.info(f"同步连接池 [{name}] 已关闭")

    for name, engine in async_engines.items():
        await engine.dispose()
        logger.info(f"异步连接池 [{name}] 已关闭")