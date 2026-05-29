import sqlite3


# 建立数据库连接
conn = sqlite3.connect('test_transaction.db')
# 创建游标
cursor = conn.cursor()

# 使用with语句自动管理事务
conn = sqlite3.connect('test.db')
cursor = conn.cursor()
with conn:  # with语句自动处理事务
    cursor.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
    cursor.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
    print("事务自动提交")
# 连接会在with块结束后自动关闭
print("连接已关闭")