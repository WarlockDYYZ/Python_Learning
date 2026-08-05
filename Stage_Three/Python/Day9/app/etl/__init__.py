from Stage_Three.Python.Day9.app.config import settings
from Stage_Three.Python.Day9.app.etl.db_pool import init_sync_pool, init_async_pool


# 初始化业务MySQL源库连接
init_sync_pool("biz_mysql", settings.BIZ_MYSQL_SYNC_URL)
init_async_pool("biz_mysql", settings.BIZ_MYSQL_ASYNC_URL)

# 初始化PostgreSQL用户标签源库连接
init_sync_pool("user_pg", settings.USER_PG_SYNC_URL)
init_async_pool("user_pg", settings.USER_PG_ASYNC_URL)

# 初始化目标分析库连接（复用之前的behavior_analysis库）
init_sync_pool("target_mysql", settings.SQLALCHEMY_DATABASE_URL)
init_async_pool("target_mysql", settings.SQLALCHEMY_ASYNC_URL)