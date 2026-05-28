import sqlite3

# 建立数据库连接（文件会自动创建）
conn = sqlite3.connect('mydatabase.db')
conn.row_factory = sqlite3.Row
# 创建游标
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE orders2 (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- SQLite 不支持 AUTO_INCREMENT
    customer_id INT NOT NULL
);
''')

cursor.execute('''
INSERT INTO orders2 (customer_id)
VALUES
(1),
(1),
(2),
(2),
(3),
(3),
(4),
(4),
(5),
(5),
(6),
(6),
(7),
(7),
(8),
(8),
(9),
(9),
(10),
(10);
''')

# 提交保存
conn.commit()

# 关闭连接
cursor.close()
conn.close()