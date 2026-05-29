import sqlite3


# 1. 建立数据库连接
# 建立数据库连接（文件会自动创建）
conn = sqlite3.connect('test_index.db')
# 创建游标
cursor = conn.cursor()

# 创建 users 表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT,
        age INTEGER
    )
''')
data_list = []
for i in range(1, 21):
    if i == 1:
        data_list.append(('张三', 'zhangsan@example.com', 25))
    else:
        data_list.append((f'User_{i}', f'user{i}@example.com', 20 + i))
cursor.executemany('INSERT INTO users (name, email, age) VALUES (?, ?, ?)', data_list)


# 2. 创建索引
# 创建普通索引
cursor.execute("CREATE INDEX idx_name ON users(name)")
# 创建唯一索引
cursor.execute("CREATE UNIQUE INDEX idx_email ON users(email)")
# 创建复合索引
cursor.execute("CREATE INDEX idx_name_age ON users(name, age)")
# 使用IF NOT EXISTS避免重复创建, 这条语句因为索引名与第一条索引名相同，所以该索引不会创建，直接跳过该语句不报错
cursor.execute("CREATE INDEX IF NOT EXISTS idx_name ON users(name)")
# 提交事务
conn.commit()


# 3. 查看索引信息
# 查询sqlite_master系统表
cursor.execute("""
    SELECT name, sql
    FROM sqlite_master
    WHERE type = 'index' AND tbl_name = 'users'
""")
for index in cursor:
    print(f"索引名: {index[0]}")
    print(f"创建语句: {index[1]}")
# 使用.indices命令（需要在SQLite命令行环境）
# 注意：这里需要使用特殊的方式执行
cursor.execute("SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name='users'")
print("\n索引列表：")
for row in cursor.fetchall():
    print(row[0])


# 4. 删除索引
# 删除索引
cursor.execute("DROP INDEX idx_name")
# 使用IF EXISTS避免错误
cursor.execute("DROP INDEX IF EXISTS idx_name")
# 提交事务
conn.commit()


# 5. 性能对比测试
import time

# 测试无索引查询性能
start_time = time.time()
cursor.execute("SELECT * FROM users WHERE name = '张三'")
result = cursor.fetchall()
no_index_time = time.time() - start_time
print(f"\n无索引查询时间: {no_index_time:.4f}秒")

# 创建索引
cursor.execute("CREATE INDEX idx_name ON users(name)")
conn.commit()
# 测试有索引查询性能
start_time = time.time()
cursor.execute("SELECT * FROM users WHERE name = '张三'")
result = cursor.fetchall()
with_index_time = time.time() - start_time
print(f"有索引查询时间: {with_index_time:.4f}秒")

# 性能提升
improvement = (no_index_time - with_index_time) / no_index_time * 100
print(f"性能提升: {improvement:.1f}%")

# 删除索引
cursor.execute("DROP INDEX idx_name")
conn.commit()