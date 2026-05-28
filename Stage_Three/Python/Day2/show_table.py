import sqlite3

# 1. 连接数据库并开启外键约束
conn = sqlite3.connect('mydatabase.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

try:
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for user in users:
        # 直接使用字符串键名访问字段
        print(f"用户ID: {user['user_id']}, 用户名: {user['username']}, 国家: {user['country']}")

    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    for order in orders:
        # 直接使用字符串键名访问字段
        print(f"订单ID: {order['order_id']}, 金额: {order['amount']}, "
              f"下单时间: {order['order_date']}, "
              f"用户名: {order['user_id']}, 客户ID: {order['customer_id']}")

except Exception as e:
    print(f"发生未知错误: {e}")
    conn.rollback()
finally:
    # 5. 关闭连接释放资源
    conn.close()