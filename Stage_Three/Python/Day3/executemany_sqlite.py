import sqlite3


# 建立数据库连接
conn = sqlite3.connect('test_transaction.db')
# 创建游标
cursor = conn.cursor()

try:
    conn.execute("BEGIN TRANSACTION")
    # 准备数据
    users = []
    for i in range(1, 1001):
        users.append((f'用户{i}', i % 30 + 18, f'user{i}@example.com'))
    # 批量插入
    cursor.executemany("INSERT INTO users (name, age, email) VALUES (?, ?, ?)", users)
    # 批量更新
    cursor.execute("UPDATE users SET age = age + 1 WHERE age < 25")
    conn.commit()
    print("批量插入1000条数据成功")
except Exception as e:
    conn.rollback()
    print(f"批量操作失败，错误: {e}")
finally:
    cursor.close()
    conn.close()