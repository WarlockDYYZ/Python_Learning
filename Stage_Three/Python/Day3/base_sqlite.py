import sqlite3


# 建立数据库连接
conn = sqlite3.connect('test_transaction.db')
# 创建游标
cursor = conn.cursor()

try:
    # 开启事务
    conn.execute("BEGIN TRANSACTION")
    # 执行SQL操作
    cursor.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
    cursor.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
    # 提交事务
    conn.commit()
    print("事务提交成功")
except Exception as e:
    # 回滚事务
    conn.rollback()
    print(f"事务回滚，错误信息: {e}")
finally:
    # 关闭游标和连接
    cursor.close()
    conn.close()