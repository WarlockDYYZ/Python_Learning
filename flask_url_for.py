from flask import Flask, url_for
app = Flask(__name__)

@app.route('/')
def index():
    return 'index'

@app.route('/login')
def login():
    return 'login'

@app.route('/user/<username>')
def profile(username):
        return f'{username}\'s profile'  # profile n. 人物简介

# 在上下文中测试URL生成逻辑
with app.test_request_context():
    # 生成指向index视图的URL
    print(url_for('index'))  # 输出：/
    # 生成指向login视图的URL
    print(url_for('login'))  # 输出：/login
    # 生成带查询参数的URL
    print(url_for('login', next='/'))  # 输出：/login?next=/
    # 生成带动态路径参数的URL
    print(url_for('profile', username='John Doe'))  # 输出：/user/John%20Doe