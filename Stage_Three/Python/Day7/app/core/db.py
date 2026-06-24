# app/core/db.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv


# 加载环境变量
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://username:password@localhost:5432/fastapi_demo")

# 1. 创建异步数据库引擎，配置连接池
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,  # 连接池常规大小，建议设为CPU核心数×2
    max_overflow=0,  # 禁止创建溢出连接，避免打爆数据库连接上限
    pool_pre_ping=True,  # 连接池心跳检测，自动剔除僵死连接，避免网络闪断异常
    pool_recycle=3600,  # 连接回收时间（秒），定期释放长时间空闲连接
    echo=False  # 生产环境关闭SQL日志打印，避免额外I/O开销
)

# 2. 创建异步会话工厂，用于生成数据库会话
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # 提交事务后，不过期ORM模型对象，便于后续读取属性
    autoflush=False  # 禁用自动刷新，由业务逻辑主动控制事务刷新时机
)

# 3. 声明ORM模型基类
class Base(DeclarativeBase):
    pass