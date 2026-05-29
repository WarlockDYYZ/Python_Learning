import pymysql


# 1. 建立数据库连接
# 建立数据库连接
conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='your_password',
    database='test_db',
    charset='utf8mb4'
)
# 创建游标
cursor = conn.cursor()


# 2. 创建索引
# 创建普通索引
cursor.execute("CREATE INDEX idx_name ON users(name)")
# 创建唯一索引
cursor.execute("CREATE UNIQUE INDEX idx_email ON users(email)")
# 创建复合索引
cursor.execute("CREATE INDEX idx_name_age ON users(name, age)")
# 创建全文索引
cursor.execute("CREATE FULLTEXT INDEX idx_content ON articles(content)")
# 提交事务
conn.commit()


# 3. 查看索引信息
# 使用SHOW INDEX查看索引
cursor.execute("SHOW INDEX FROM users")
index_info = cursor.fetchall()
for index in index_info:
    print(f"索引名: {index[2]}, 列名: {index[4]}, 唯一性: {'是' if index[1] == 0 else '否'}")
# 查询information_schema获取索引信息
cursor.execute("""
    SELECT index_name, column_name, non_unique
    FROM information_schema.statistics
    WHERE table_name = 'users' AND table_schema = 'test_db'
""")
index_info = cursor.fetchall()
for index in index_info:
    print(f"索引名: {index[0]}, 列名: {index[1]}, 唯一性: {'是' if index[2] == 0 else '否'}")


# 4. 删除索引
# 删除普通索引
cursor.execute("DROP INDEX idx_name ON users")
# 删除唯一索引
cursor.execute("DROP INDEX idx_email ON users")
# 删除复合索引
cursor.execute("DROP INDEX idx_name_age ON users")
# 提交事务
conn.commit()


# 5. 性能对比测试
import time
# 测试无索引查询性能
start_time = time.time()
cursor.execute("SELECT * FROM users WHERE name = '张三'")
result = cursor.fetchall()
no_index_time = time.time() - start_time
print(f"无索引查询时间: {no_index_time:.4f}秒")
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
cursor.execute("DROP INDEX idx_name ON users")
conn.commit()