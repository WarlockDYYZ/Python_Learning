from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_migrate import Migrate

# 初始化SQLAlchemy ORM扩展
db = SQLAlchemy()
# 初始化Flask-Login用户会话管理扩展
login_manager = LoginManager()
# 初始化Flask-WTF的CSRF保护扩展
csrf = CSRFProtect()
# 初始化Flask-Migrate数据库迁移扩展
migrate = Migrate()