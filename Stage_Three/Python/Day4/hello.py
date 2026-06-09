# 导入 Flask 类，该类是 Flask 应用的核心
from flask import Flask


# 创建 Flask 应用实例，__name__ 指向当前模块的路径
app = Flask(__name__)
# 定义路由：将根 URL 绑定到 hello_world 视图函数
@app.route("/")
def hello_world():
    # 返回的字符串会被浏览器解析为 HTML 内容
    return "<p>Hello, World!</p>"