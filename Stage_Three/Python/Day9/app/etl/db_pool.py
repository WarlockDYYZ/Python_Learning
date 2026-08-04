# app/etl/db_pool.py
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings
from typing import Dict


# 同步连接池字典
sync_pools: Dict[str, sessionmaker] = {}
# 异步连接池字典
async_pools: Dict[str, sessionmaker] = {}

def init_sync_pool(source_name: str, db_url: str):
    """初始化同步数据库连接池"""
    engine = create_engine(
        db_url,
        pool_pre_ping=True,  # 心跳检测，避免断连
        pool_size=10,         # 连接池默认大小
        max_overflow=20,      # 超出池大小的额外连接数
        echo=settings.DEBUG
    )
    sync_pools[source_name] = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_async_pool(source_name: str, db_url: str):
    """初始化异步数据库连接池"""
    engine = create_async_engine(
        db_url,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        echo=settings.DEBUG
    )
    async_pools[source_name] = sessionmaker(
        autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
    )

def get_sync_session(source_name: str) -> Session:
    """获取同步数据库会话（供ETL全量同步使用）"""
    return sync_pools[source_name]()

def get_async_session(source_name: str) -> AsyncSession:
    """获取异步数据库会话（供ETL增量同步使用）"""
    return async_pools[source_name]()