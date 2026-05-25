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


# 关闭游标
cursor.close()
print("游标已关闭")
# 关闭连接
conn.close()
print("数据库连接已关闭")
