from datetime import datetime, timezone
from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    """用户数据库模型，对应user表"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    # created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime)
    # 定义关系：一个用户可以拥有多个文件，用户删除时会级联删除该用户的所有文件
    files = db.relationship('File', backref='author', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        """设置密码，将明文密码转换为哈希字符串存储"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """验证密码，对比用户输入的明文密码和数据库中的哈希字符串"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """定义模型的字符串表示，方便在调试时打印对象信息"""
        return f'<User {self.username}>'

class File(db.Model):
    """文件数据库模型，对应file表"""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False, index=True)
    filesize = db.Column(db.Integer, nullable=False)  # 文件大小，单位为字节
    upload_time = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    # 外键关联user表的id字段，指明该文件属于哪个用户
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<File {self.filename}>'