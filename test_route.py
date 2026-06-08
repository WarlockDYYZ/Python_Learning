from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    # 视图函数的返回值会被封装成 HTTP 响应返回给客户端
    return 'Index Page'