from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


# 创建MySQL连接池
engine = create_engine(
    'mysql+pymysql://root:your_password@localhost/test_db',
    pool_size=10,            # 连接池大小
    max_overflow=5,          # 超过pool_size的连接数
    pool_recycle=3600,        # 连接回收时间（秒）
    pool_pre_ping=True,       # 连接使用前检查有效性
    echo=False               # 是否打印SQL日志
)

# 创建基类
Base = declarative_base()


# 定义模型
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    age = Column(Integer)
    email = Column(String(100))


# 创建会话工厂
Session = sessionmaker(bind=engine)
# 创建会话（自动使用连接池）
session = Session()

# 查询操作
users = session.query(User).filter(User.age > 20).limit(10).all()
for user in users:
    print(f"用户ID: {user.id}, 姓名: {user.name}, 年龄: {user.age}")
# 插入操作
new_user = User(name='新用户', age=25, email='new@example.com')
session.add(new_user)
session.commit()
# 批量插入
new_users = [
    User(name=f'用户{i}', age=i%30+18, email=f'user{i}@example.com')
    for i in range(10001, 10011)
]

session.add_all(new_users)
session.commit()
session.close()  # 关闭会话（归还连接）