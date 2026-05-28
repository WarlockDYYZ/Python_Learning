import time
import pymysql
import sqlite3


# MySQL 配置与测试
db_config = {
    "host": "127.0.0.1",      # 数据库主机地址
    "port": 3306,             # MySQL默认端口
    "user": "root",           # 用户名
    "password": "123456", # 密码
    "database": "data_analysis",    # 数据库名
    "charset": "utf8mb4"      # 字符集，推荐使用utf8mb4支持emoji
}

# MySQL 连接
conn = pymysql.connect(**db_config)
cursor = conn.cursor()

# 测试 MySQL GROUP BY性能 (重复执行 1000 次相同 SQL 语句)
start_time = time.time()
for _ in range(1000):
    cursor.execute("SELECT customer_id, COUNT(*) FROM orders GROUP BY customer_id")
mysql_time = time.time() - start_time

# 关闭 MySQL
cursor.close()
conn.close()


# SQLite 测试，建立数据库连接（文件已创建）
conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# 测试SQLite GROUP BY性能
start_time = time.time()
for _ in range(1000):
    cursor.execute("SELECT customer_id, COUNT(*) FROM orders GROUP BY customer_id")
sqlite_time = time.time() - start_time

# 关闭
cursor.close()
conn.close()


print(f"\n性能对比：")
print(f"MySQL GROUP BY 1000次耗时: {mysql_time:.3f}秒")
print(f"SQLite GROUP BY 1000次耗时: {sqlite_time:.3f}秒")
print(f"性能差异: {mysql_time/sqlite_time:.1f}倍")