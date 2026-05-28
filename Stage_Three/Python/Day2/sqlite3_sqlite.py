import sqlite3

# 建立数据库连接（文件会自动创建）
conn = sqlite3.connect('mydatabase.db')
conn.row_factory = sqlite3.Row
# 创建游标
cursor = conn.cursor()


# 查询每个客户的订单统计
group_sql = """
SELECT
    customer_id,
    COUNT(order_id) AS total_orders,
    SUM(amount) AS total_amount
FROM orders
GROUP BY customer_id
HAVING total_orders >= 2
ORDER BY total_amount DESC;
"""
cursor.execute(group_sql)
results = cursor.fetchall()

print("客户订单统计（订单数≥2）：")
for row in results:
    print(f"客户ID: {row['customer_id']}, 订单数: {row['total_orders']}, 总金额: {row['total_amount']}")


# 查询用户及其订单信息（左连接）
join_sql = """
SELECT
    u.user_id,
    u.username,
    o.order_id,
    o.order_date,
    o.amount
FROM users AS u
LEFT JOIN orders AS o
ON u.user_id = o.user_id
WHERE u.country = ?
ORDER BY u.user_id, o.order_date;
"""
# 使用参数化查询（?占位符）
cursor.execute(join_sql, ("China",))
results = cursor.fetchall()
print("\n用户订单信息（中国用户）：")
for row in results:
    print(f"用户ID: {row['user_id']}, 用户名: {row['username']}, "
          f"订单ID: {row['order_id']}, 日期: {row['order_date']}, 金额: {row['amount']}")


# SQLite支持非标准的连接语法
non_standard_sql = """
SELECT
    u.user_id,
    u.username,
    o.order_id
FROM users AS u
NATURAL LEFT OUTER JOIN orders AS o
WHERE u.country = ?;
"""
cursor.execute(non_standard_sql, ("USA",))
results = cursor.fetchall()
print("\nSQLite特有语法示例：")
for row in results:
    print(f"用户ID: {row['user_id']}, 用户名: {row['username']}, 订单ID: {row['order_id']}")

# # 检查 users 表的实际结构
# cursor.execute("PRAGMA table_info(users);")
# print(cursor.fetchall())
# # 输出示例：[(0, 'user_id', 'INTEGER', ...), (1, 'username', 'TEXT', ...), (2, 'country', 'TEXT', ...)]
