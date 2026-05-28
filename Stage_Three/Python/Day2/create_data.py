import sqlite3


# 连接数据库（不存在会自动创建）
conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()

# ----------------------
# 1. 创建表
# ----------------------
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    country TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_date TEXT NOT NULL,
    amount REAL NOT NULL,
    user_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL
)
''')

# ----------------------
# 2. 插入 users 数据
# ----------------------
users_data = [
    ('张三', 'China'),
    ('李四', 'China'),
    ('Jack', 'USA'),
    ('Emma', 'USA')
]
cursor.executemany('''
INSERT INTO users (username, country)
VALUES (?, ?)
''', users_data)

# ----------------------
# 3. 插入 orders 数据
# ----------------------
orders_data = [
    ('2025-01-01', 150.50, 1, 101),
    ('2025-01-02', 200.99, 1, 101),
    ('2025-01-03', 350.00, 2, 102),
    ('2025-01-04', 120.00, 2, 102),
    ('2025-01-05', 480.99, 3, 103),
    ('2025-01-06', 620.50, 3, 103)
]
cursor.executemany('''
INSERT INTO orders (order_date, amount, user_id, customer_id)
VALUES (?, ?, ?, ?)
''', orders_data)

# 提交保存
conn.commit()

# ----------------------
# 关闭连接
# ----------------------
cursor.close()
conn.close()