from flask import Flask, render_template, redirect, url_for, flash
from forms import LoginForm, RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

@app.route('/login', methods=['GET', 'POST'])
def login():
    # 实例化登录表单对象
    form = LoginForm()
    # 验证表单提交是否合法
    if form.validate_on_submit():
        # 表单验证通过，获取用户输入的数据
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data
        # 此处添加具体的用户验证逻辑
        flash('登录成功！', 'success')
        return redirect(url_for('dashboard'))
    # 如果是GET请求或验证失败，重新渲染登录表单页面
    return render_template('login3.html', form=form)

@app.route('/dashboard')
def dashboard():
    return 'dashboard'