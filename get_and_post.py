from flask import Flask, request, render_template, redirect, url_for
app = Flask(__name__)

# 路由同时支持GET和POST请求
@app.route('/login', methods=['GET', 'POST'])
def login():
    # 根据请求方法执行不同的逻辑
    if request.method == 'POST':
        # 处理POST请求提交的表单数据
        username = request.form.get('username')
        password = request.form.get('password')
        # 此处添加实际的账号密码验证逻辑
        if username == 'admin' and password == 'secret':
            # 验证通过，重定向到首页
            return redirect(url_for('index'))
        else:
            # 验证失败，返回错误信息
            return 'Invalid credentials'
    # GET请求默认返回登录表单页面
    return render_template('login.html')

# 根目录显示内容
@app.route('/')

# index 界面
@app.route('/index')
def index():
    return render_template('index.html')
