from dbutils.pooled_db import PooledDB
import pymysql


# 创建MySQL连接池
pool = PooledDB(
    creator=pymysql,  # 使用pymysql作为数据库驱动
    maxconnections=15,  # 最大连接数
    mincached=5,       # 初始化时创建的空闲连接数
    maxcached=10,      # 最多保持的空闲连接数
    blocking=True,      # 当连接池耗尽时，是否阻塞等待
    maxusage=100,      # 单个连接的最大使用次数
    setsession=[],      # 连接创建后执行的SQL命令
    ping=0,            # 0=None=never, 1=default, 2=when idle, 4=always
    host='localhost',
    port=3306,
    user='root',
    password='your_password',
    database='pooled_db',
    charset='utf8mb4'
)