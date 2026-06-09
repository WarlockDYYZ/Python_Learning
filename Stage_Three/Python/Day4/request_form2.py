from flask import Flask, request, render_template, redirect, url_for, flash, session
app = Flask(__name__)
# 为了使用flash()函数存储闪现消息，需要设置SECRET_KEY
app.config['SECRET_KEY'] = 'your-secret-key'

@app.route('/login', methods=['GET', 'POST'])
def login():
    # 初始化错误信息
    error = None
    if request.method == 'POST':
        # 从请求体中获取表单数据
        username = request.form.get('username')
        password = request.form.get('password')
        # 手动编写表单验证逻辑
        if not username:
            error = '用户名不能为空'
        elif not password:
            error = '密码不能为空'
        elif username != 'admin' or password != 'secret':
            error = '用户名或密码错误'
        else:
            # 验证通过，设置Session并跳转至仪表板页面
            session['user_id'] = username
            flash('登录成功！', 'success')
            return redirect(url_for('dashboard'))
    # 如果是GET请求或验证失败，重新渲染登录表单页面
    return render_template('login2.html', error=error)

@app.route('/dashboard')
def dashboard():
    return 'dashboard'