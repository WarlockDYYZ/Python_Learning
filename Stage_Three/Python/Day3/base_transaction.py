import pymysql


# 建立数据库连接
conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='your_password',
    database='transaction_db',
    charset='utf8mb4'
)
# 创建游标
cursor = conn.cursor()

try:
    # 开启事务（关闭自动提交）
    conn.autocommit(False)

    # 执行SQL操作
    cursor.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
    cursor.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")

    # 模拟错误（取消注释会触发异常）
    # raise Exception("模拟错误，回滚事务")

    # 提交事务
    conn.commit()
    print("事务提交成功")

except Exception as e:
    # 回滚事务
    conn.rollback()
    print(f"事务回滚，错误信息: {e}")

finally:
    # 恢复自动提交模式
    conn.autocommit(True)
    # 关闭游标和连接
    cursor.close()
    conn.close()