import sqlite3

# 连接数据库
conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()

# ===================== 建表 + 插入数据 =====================
cursor.executescript('''
CREATE TABLE IF NOT EXISTS users3 (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    register_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS orders3 (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

INSERT INTO users3 (register_date)
VALUES
('2023-01-10'),
('2023-01-15'),
('2023-02-01'),
('2023-02-10'),
('2023-03-01');

INSERT INTO orders3 (user_id, order_date, amount)
VALUES
(1, '2023-01-12', 99.50),
(1, '2023-02-15', 120.00),
(1, '2023-03-20', 88.00),

(2, '2023-01-18', 150.75),
(2, '2023-02-22', 200.50),

(3, '2023-02-05', 50.00),
(3, '2023-03-10', 45.50),
(3, '2023-04-15', 60.25),

(4, '2023-02-15', 300.00),
(4, '2023-03-18', 250.50),

(5, '2023-03-05', 80.75),
(5, '2023-04-02', 95.25);
''')

conn.commit()


cursor.close()
conn.close()