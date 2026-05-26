import pymysql


# 数据库连接配置
db_config = {
    "host": "127.0.0.1",      # 数据库主机地址
    "port": 3306,             # MySQL默认端口
    "user": "root",           # 用户名
    "password": "123456", # 密码
    "database": "test_db",    # 数据库名
    "charset": "utf8mb4"      # 字符集，推荐使用utf8mb4支持emoji
}

# 建立连接
conn = pymysql.connect(**db_config)

print("数据库连接成功")


# 创建游标（默认返回元组类型结果）
cursor = conn.cursor()
print("游标创建成功")
# 如果需要返回字典类型结果，可以指定cursorclass
# cursor = conn.cursor(pymysql.cursors.DictCursor)


# 执行查询语句
sql = "SELECT VERSION()"
cursor.execute(sql)
# 获取查询结果
result = cursor.fetchone()
print(f"MySQL版本: {result[0]}")


# 执行插入操作
insert_sql = "INSERT INTO user (username, password) VALUES (%s, %s)"
try:
    cursor.execute(insert_sql, ("test_user", "123456"))
    conn.commit()  # 提交事务
    print("数据插入成功")
except Exception as e:
    conn.rollback()  # 回滚事务
    print(f"插入失败: {e}")


# 安全的参数化查询
username = "test_user"
password = "123456"
query_sql = "SELECT * FROM user WHERE username = %s AND password = %s"
try:
    cursor.execute(query_sql, (username, password))

    # 查看结果, 取出所有数据
    result = cursor.fetchall()
    if result:
        print("查询结果：", result)
    else:
        print("结果为空")
except Exception as e:
    print(f"查询失败: {e}")


# 批量插入数据（速度提升10-50倍）
data = [
    ("张三", 20),
    ("李四", 21),
    ("王五", 22)
]
insert_sql = "INSERT INTO user2 (name, age) VALUES (%s, %s)"
try:
    cursor.executemany(insert_sql, data)
    conn.commit()
    print("数据插入成功")
except Exception as e:
    conn.rollback()
    print(f"插入失败: {e}")


# 关闭游标
cursor.close()
print("游标已关闭")


# 关闭连接
conn.close()
print("数据库连接已关闭")
