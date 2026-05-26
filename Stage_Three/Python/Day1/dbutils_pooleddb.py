import pymysql
from dbutils.pooled_db import PooledDB


# 配置连接池
pool = PooledDB(
    creator=pymysql,      # 使用pymysql作为数据库驱动
    maxconnections=10,    # 最大连接数
    mincached=2,          # 初始化时创建的空闲连接数
    maxcached=5,          # 最多保持的空闲连接数
    maxshared=3,          # 最大共享连接数
    blocking=True,        # 连接耗尽时是否阻塞等待
    host="localhost",
    port=3306,
    user="root",
    password="123456",
    database="test_db",
    charset="utf8mb4"
)


# 从连接池获取连接
def get_connection():
    conn = pool.connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    return conn, cursor


# 使用连接池执行查询
def query_with_pool():
    conn, cursor = get_connection()
    try:
        cursor.execute("SELECT COUNT(*) AS count FROM user;")
        result = cursor.fetchone()
        print(f"用户总数: {result['count']}")
    finally:
        # 归还连接到连接池（不真正关闭）
        cursor.close()
        conn.close()


# 调用代码
if __name__ == '__main__':
    print("正在从连接池获取连接并查询数据...")
    query_with_pool()  # 调用函数
    print("执行完成！")
