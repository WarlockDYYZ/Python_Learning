from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# 配置MySQL连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@localhost/test_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭追踪修改

# 初始化数据库对象
db = SQLAlchemy(app)

# 定义模型
class User(db.Model):

    # autoincrement=True 设置为自增字段，SQLAlchemy 会根据不同的数据库原生特性，设置自增
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


    def __repr__(self):
        return f'<User {self.username}>'


    def is_active(self):
        return self.status == 'active'