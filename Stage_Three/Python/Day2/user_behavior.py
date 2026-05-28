import sqlite3


# 建立数据库连接（文件会自动创建）
conn = sqlite3.connect('mydatabase.db')
conn.row_factory = sqlite3.Row
# 创建游标
cursor = conn.cursor()


# 用户行为分析
user_behavior_sql = """
SELECT
    u.user_id,
    u.register_date,
    COUNT(DISTINCT o.order_id) AS order_count,
    SUM(o.amount) AS lifetime_value,
    AVG(o.amount) AS avg_order_value,
    MAX(o.order_date) AS last_order_date,
    (JulianDay('now') - JulianDay(MAX(o.order_date))) AS days_since_last_order
FROM users3 AS u
LEFT JOIN orders3 AS o
    ON u.user_id = o.user_id
GROUP BY u.user_id
HAVING order_count >= 2  -- 至少有2次购买
ORDER BY lifetime_value DESC;
"""
cursor.execute(user_behavior_sql)
results = cursor.fetchall()


print("\n用户行为分析（复购用户）：")
for row in results[:10]:  # 显示前10名
    print(f"用户ID: {row['user_id']}, 注册日期: {row['register_date']}, "
          f"订单数: {row['order_count']}, 生命周期价值: {row['lifetime_value']}, "
          f"平均客单价: {row['avg_order_value']}, 最近购买: {row['last_order_date']}")


# 计算用户分层（RFM模型简化版）
print("\n用户分层分析：")
for row in results[:10]:
    # 基于最近购买时间和订单数进行分层
    if row['days_since_last_order'] < 30 and row['order_count'] >= 5:
        level = "重要价值客户"
    elif row['days_since_last_order'] < 30 and row['order_count'] >= 2:
        level = "活跃客户"
    elif row['days_since_last_order'] < 90:
        level = "回流客户"
    else:
        level = "流失客户"

    print(f"用户ID: {row['user_id']}, 分层: {level}")