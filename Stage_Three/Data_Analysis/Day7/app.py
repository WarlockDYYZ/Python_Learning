from flask import Flask, session
from flask_session import Session
from extensions import RedisClient  # 导入封装的工具类

# 初始化Flask应用
app = Flask(__name__)
# 初始化Redis客户端，复用全局连接池
redis_client = RedisClient(
    host=app.config["REDIS_HOST"],
    port=app.config["REDIS_PORT"],
    db=app.config["REDIS_DB"],
    password=app.config.get("REDIS_PASSWORD"),
    max_connections=20
)
# 将Redis客户端绑定到应用上下文，所有路由中统一使用
app.extensions["redis"] = redis_client


# 配置Flask-Session，使用Redis作为会话存储后端
app.config.update(
    SESSION_TYPE="redis",  # 设置会话存储类型为Redis
    SESSION_REDIS=redis_client.client,  # 使用预配置的Redis客户端
    SESSION_PERMANENT=False,
    SESSION_USE_SIGNER=True,  # 对会话cookie签名加密，防止篡改
    SESSION_KEY_PREFIX="flask:session:",  # Redis键名前缀，区分不同业务
    PERMANENT_SESSION_LIFETIME=1800  # 会话超时时间30分钟
)
# 初始化会话扩展，绑定到Flask应用
Session(app)

# 会话使用示例：登录时设置会话数据
@app.route("/login")
def login():
    session["user_id"] = 1001
    session["username"] = "test_user"
    return "login success"

# 接口中获取会话数据
@app.route("/profile")
def profile():
    user_id = session.get("user_id")
    if not user_id:
        return "unauthorized", 401
    return f"user profile: {user_id}"