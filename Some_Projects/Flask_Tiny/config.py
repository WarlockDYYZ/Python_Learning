import os
from datetime import timedelta


class Config:
    # 基础安全配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    # 数据库配置，优先从环境变量中读取数据库连接字符串
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    # 关闭SQLAlchemy的修改跟踪，避免弹出警告信息
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 文件上传配置
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 限制最大上传文件为16MB
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

    # Session配置
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)  # Session过期时间为2小时
    SESSION_COOKIE_SECURE = False  # 开发环境下设置为False，生产环境下设置为True
    SESSION_COOKIE_HTTPONLY = True  # 禁止JS读取Session Cookie，防止XSS攻击
    SESSION_COOKIE_SAMESITE = 'Lax'  # 开启CSRF保护