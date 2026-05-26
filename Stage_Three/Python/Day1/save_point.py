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
cursor = conn.cursor()

# 使用保存点的事务示例
try:
    # 第一步操作
    cursor.execute("INSERT INTO user (username, password) VALUES ('test1', '123');")
    # 创建保存点（正确写法！）
    cursor.execute("SAVEPOINT sp1")
    # 第二步操作
    cursor.execute("INSERT INTO user (username, password) VALUES ('test2', '456');")
    # 回滚到保存点（正确写法！）
    cursor.execute("ROLLBACK TO sp1")
    print("已回滚到保存点 sp1")
    # 提交最终结果
    conn.commit()
    print("事务提交完成")
except Exception as e:
    conn.rollback()
    print(f"事务失败: {e}")
