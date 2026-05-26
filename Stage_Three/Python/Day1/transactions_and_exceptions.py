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

# 转账事务示例
def transfer(from_uid, to_uid, amount):
    try:
        # 开启事务
        conn.begin()

        # 使用 with 语句，退出缩进后会自动关闭游标
        with conn.cursor() as cursor:
            # 业务校验：检查余额是否充足
            check_sql = "SELECT balance FROM account WHERE user_id = %s"
            cursor.execute(check_sql, (from_uid,))
            balance = cursor.fetchone()[0]
            if balance < amount:
                raise ValueError("余额不足")

            sql1 = "UPDATE account SET balance = balance - %s WHERE user_id = %s"
            cursor.execute(sql1, (amount, from_uid))

            sql2 = "UPDATE account SET balance = balance + %s WHERE user_id = %s"
            cursor.execute(sql2, (amount, to_uid))

        conn.commit()
        print("转账成功")
    except Exception as e:
        conn.rollback()
        print(f"转账失败，已回滚: {e}")
    # finally:
        # 如果使用的是短连接（每次转账新建一个连接），这里也应该关闭连接：
        # if conn:
        #     conn.close()
