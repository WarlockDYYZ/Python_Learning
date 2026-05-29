import sqlite3


# 建立数据库连接
conn = sqlite3.connect('test_transaction.db')
# 创建游标
cursor = conn.cursor()

# 虽然SQLite仅支持SERIALIZABLE，但可以尝试设置
try:
    conn = sqlite3.connect('test.db', isolation_level='SERIALIZABLE')
    print("已设置隔离级别为SERIALIZABLE")

except Exception as e:
    print(f"设置隔离级别失败: {e}")

# 尝试设置其他隔离级别（会失败）
try:
    conn = sqlite3.connect('test.db', isolation_level='READ COMMITTED')
except Exception as e:
    print(f"不支持的隔离级别: {e}")