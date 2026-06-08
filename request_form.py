from flask import Flask, request, render_template, redirect, url_for
app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # 从请求体中获取表单数据
        username = request.form.get('username')
        password = request.form.get('password')
        # 验证逻辑
        if not username or not password:
            error = '用户名和密码都是必填项'
        elif username != 'admin' or password != 'secret':
            error = '用户名或密码错误'
        else:
            # 验证通过，重定向到仪表板页面
            return redirect(url_for('dashboard'))
    # 渲染登录模板，传递错误信息（如果存在）
    return render_template('login.html', error=error)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return 'The dashboard page'