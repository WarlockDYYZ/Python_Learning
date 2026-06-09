from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from exts import db


class User(db.Model):
    """用户模型类，对应数据库中的 users 表"""
    __tablename__ = 'users'  # 自定义表名（可选，默认会是 user）

    # 主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 用户名：最大长度20，不能为空，必须唯一
    username = db.Column(db.String(20), nullable=False, unique=True)

    # 邮箱：最大长度120，不能为空，必须唯一
    email = db.Column(db.String(120), nullable=False, unique=True)

    # 密码：数据库中绝对不能存明文，必须存哈希值
    password_hash = db.Column(db.String(256), nullable=False)

    # 注册时间：默认获取当前时间
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        """方便在控制台打印用户对象时显示用户名"""
        return f'<User {self.username}>'

    # ================= 密码加密与校验方法 =================
    @property
    def password(self):
        """密码属性不可直接读取"""
        raise AttributeError('密码是不可读的！')

    @password.setter
    def password(self, raw_password):
        """将明文密码进行哈希加密后存入数据库"""
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        """校验用户输入的明文密码与数据库中的哈希值是否匹配"""
        return check_password_hash(self.password_hash, raw_password)