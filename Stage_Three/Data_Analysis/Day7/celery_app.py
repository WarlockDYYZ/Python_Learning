from flask import Flask
from celery import Celery
from extensions import RedisClient

app = Flask(__name__)
# 初始化Redis客户端
redis_client = RedisClient(
    host=app.config["REDIS_HOST"],
    port=app.config["REDIS_PORT"],
    db=app.config["REDIS_DB"],
    password=app.config.get("REDIS_PASSWORD"),
    max_connections=20
)

# 初始化Celery，将Redis作为消息中间件
celery = Celery(
    app.import_name,
    broker=f"redis://:{app.config['REDIS_PASSWORD']}@{app.config['REDIS_HOST']}:{app.config['REDIS_PORT']}/0",
    backend=f"redis://:{app.config['REDIS_PASSWORD']}@{app.config['REDIS_HOST']}:{app.config['REDIS_PORT']}/1"
)

# 定义异步任务：模拟发送注册邮件，耗时3秒
@celery.task
def send_register_email(email: str):
    import time
    time.sleep(3)
    print(f"send register email to {email}")
    return {"status": "success", "email": email}

# Flask路由：用户注册，异步发送邮件
@app.route("/register", methods=["POST"])
def register():
    # 1. 先执行核心的用户注册逻辑
    # 2. 投递发送邮件的异步任务到Celery队列
    send_register_email.delay("test@example.com")
    # 3. 立即返回响应，不等待邮件发送结果
    return {"status": "success", "message": "register success"}