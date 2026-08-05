from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from Stage_Three.Python.Day9.app.config import settings

# 创建数据库引擎
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,          # 连接前先 ping，防止断连
    pool_size=10,                # 连接池大小
    max_overflow=20,             # 超出 pool_size 的额外连接
    echo=settings.DEBUG,         # DEBUG 模式打印 SQL
)

# 会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# 模型基类
Base = declarative_base()


def get_db():
    """FastAPI 依赖注入：获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()