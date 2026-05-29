import pymysql


# 建立数据库连接
conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='your_password',
    database='transaction_db',
    charset='utf8mb4'
)
# 创建游标
cursor = conn.cursor()

try:
    conn.autocommit(False)
    # 第一步操作
    cursor.execute("INSERT INTO users (name, age) VALUES ('张三', 20)")
    # 设置保存点
    conn.savepoint("sp1")
    # 第二步操作
    cursor.execute("INSERT INTO users (name, age) VALUES ('李四', 21)")
    # 设置另一个保存点
    conn.savepoint("sp2")
    # 第三步操作（故意出错）
    cursor.execute("INSERT INTO users (name, age) VALUES ('王五', '错误的年龄')")
    # 提交（不会执行到这里）
    conn.commit()
except Exception as e:
    # 回滚到保存点sp2
    conn.rollback("sp2")
    print("回滚到保存点 sp2，已插入张三和李四")
    # 继续执行其他操作
    cursor.execute("INSERT INTO users (name, age) VALUES ('赵六', 22)")
    # 提交最终结果
    conn.commit()
    print("最终提交成功，包含张三、李四、赵六")
finally:
    conn.autocommit(True)
    cursor.close()
    conn.close()