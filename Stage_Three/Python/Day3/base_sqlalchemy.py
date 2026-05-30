from sqlalchemy import create_engine, text


# 创建连接池
engine = create_engine(
    'mysql+pymysql://root:your_password@localhost/test_db',
    pool_size=10,
    max_overflow=5,
    pool_recycle=3600,
    pool_pre_ping=True
)
# 使用with语句自动管理连接
with engine.connect() as connection:
    # 执行查询
    result = connection.execute(text("SELECT * FROM users LIMIT 10"))

    # 处理结果
    for row in result:
        print(row)

    # 执行更新
    connection.execute(text("UPDATE users SET age = age + 1 WHERE id = 1"))
    connection.commit()
    
# 批量操作
with engine.connect() as connection:
    # 准备数据
    data = []
    for i in range(1, 10001):
        data.append((f'用户{i}', i % 30 + 18, f'user{i}@example.com'))

    # 批量插入
    connection.execute(text("""
       INSERT INTO users (name, age, email)
       VALUES (:name, :age, :email)
   """), data)
    connection.commit()
    print("批量插入10000条数据成功")