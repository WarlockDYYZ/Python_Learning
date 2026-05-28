import pymysql


# 1. 基础连接与执行
# 建立数据库连接
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="123456",
    database="customer_orders_db",
    charset="utf8mb4"
)
# 创建游标（推荐使用字典游标，结果更易处理）
cursor = conn.cursor(pymysql.cursors.DictCursor)


# 2. GROUP BY 分组查询示例
# 查询每个客户的订单总数和总金额
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
print(results)
print("客户订单统计（订单数≥2）：")
for row in results:
   print(f"客户ID: {row['customer_id']}, 订单数: {row['total_orders']}, 总金额: {row['total_amount']}")


# 3. JOIN 联表查询示例
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
WHERE u.country = %s
ORDER BY u.user_id, o.order_date;
"""
# 使用参数化查询（安全）
cursor.execute(join_sql, ("China",))
results = cursor.fetchall()
print(results)
print("n用户订单信息（中国用户）：")
for row in results:
    print(f"用户ID: {row['user_id']}, 用户名: {row['username']}, "
          f"订单ID: {row['order_id']}, 日期: {row['order_date']}, 金额: {row['amount']}")


# 4. 多表 JOIN 与分组示例
# 查询每个客户的订单数和商品类别分布
complex_sql = """
SELECT
    c.customer_id,
    c.name AS customer_name,
    COUNT(o.order_id) AS order_count,
    p.category AS product_category,
    SUM(oi.quantity * oi.unit_price) AS category_total
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
LEFT JOIN order_items AS oi
    ON o.order_id = oi.order_id
LEFT JOIN products AS p
    ON oi.product_id = p.product_id
WHERE c.country = %s
GROUP BY c.customer_id, p.category
ORDER BY order_count DESC, category_total DESC;
"""
cursor.execute(complex_sql, ("USA",))
results = cursor.fetchall()
print("n美国客户订单分析：")
for row in results:
    print(f"客户ID: {row['customer_id']}, 客户名: {row['customer_name']}, "
          f"订单数: {row['order_count']}, 类别: {row['product_category']}, 类别总金额: {row['category_total']}")