from sqlalchemy import create_engine


# 创建MySQL连接池
engine = create_engine(
    'mysql+pymysql://root:your_password@localhost/test_db',
    pool_size=10,            # 连接池大小
    max_overflow=5,          # 超过pool_size的连接数
    pool_recycle=3600,        # 连接回收时间（秒）
    pool_pre_ping=True,       # 连接使用前检查有效性
    echo=False               # 是否打印SQL日志
)

# 获取连接
connection = engine.connect()
try:
   # 执行查询
   result = connection.execute("SELECT * FROM users LIMIT 10")
   # 处理结果
   for row in result:
       print(row)
finally:
   # 关闭连接（归还到池）
   connection.close()