from dbutils.pooled_db import PooledDB
import pymysql


# 基础操作
# 创建连接池
pool = PooledDB(
    creator=pymysql,
    maxconnections=15,
    mincached=5,
    maxcached=10,
    blocking=True,
    host='localhost',
    port=3306,
    user='root',
    password='your_password',
    database='test_db',
    charset='utf8mb4'
)

# 从池中获取连接
conn = pool.connection()
try:
    # 创建游标
    cursor = conn.cursor()

    # 执行查询
    cursor.execute("SELECT * FROM users LIMIT 10")
    results = cursor.fetchall()

    # 处理结果
    for row in results:
        print(row)

    # 执行更新
    cursor.execute("UPDATE users SET age = age + 1 WHERE id = 1")
    conn.commit()
finally:
    # 关闭连接（归还到池）
    if 'cursor' in locals():
        cursor.close()
    conn.close()

# 查看连接池状态
print(f"当前连接池状态:")
print(f"  最大连接数: {pool.maxconnections}")
print(f"  当前连接数: {pool._current_connections}")
print(f"  空闲连接数: {pool._idle_connections}")
print(f"  活动连接数: {pool._active_connections}")


# 批量操作
# 批量插入10000条数据
conn = pool.connection()
cursor = conn.cursor()
try:
    # 准备数据
    data = []
    for i in range(1, 10001):
        data.append((f'用户{i}', i % 30 + 18, f'user{i}@example.com'))

    # 批量插入
    cursor.executemany("INSERT INTO users (name, age, email) VALUES (%s, %s, %s)", data)
    conn.commit()

    print("批量插入10000条数据成功")

except Exception as e:
    conn.rollback()
    print(f"批量操作失败: {e}")

finally:
    cursor.close()
    conn.close()


# 监控连接池使用情况
import time


def monitor_pool_status(pool, interval=5):
    """定期监控连接池状态"""
    while True:
        print("n连接池状态监控（每5秒更新）:")
        print(f"  时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  最大连接数: {pool.maxconnections}")
        print(f"  当前连接数: {pool._current_connections}")
        print(f"  空闲连接数: {pool._idle_connections}")
        print(f"  活动连接数: {pool._active_connections}")
        print(f"  已创建连接总数: {pool._created_connections}")
        print(f"  已销毁连接总数: {pool._destroyed_connections}")

        time.sleep(interval)


# 启动监控线程（需要导入threading）
import threading

monitor_thread = threading.Thread(target=monitor_pool_status, args=(pool, 5))
monitor_thread.daemon = True
monitor_thread.start()


# 模拟多个线程使用连接池
def worker_thread():
    conn = pool.connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        result = cursor.fetchone()
        print(f"线程{threading.get_ident()}: 用户总数 = {result[0]}")
    finally:
        conn.close()


# 启动多个工作线程
for i in range(10):
    t = threading.Thread(target=worker_thread)
    t.start()