import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory
from werkzeug.utils import secure_filename
from config import Config
from extensions import db, login_manager, csrf, migrate
from models import User, File
from forms import LoginForm, RegisterForm, UploadForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# 创建Flask应用实例
app = Flask(__name__)
# 从配置类中加载应用配置
app.config.from_object(Config)

# 初始化所有扩展
db.init_app(app)
login_manager.init_app(app)
csrf.init_app(app)
migrate.init_app(app, db)

# 配置Flask-Login的登录视图，未登录用户访问保护路由时会跳转到该页面
login_manager.login_view = 'login'
login_manager.login_message = '请先登录后再访问该页面'
login_manager.login_message_category = 'warning'

# 加载用户的回调函数，通过用户ID加载用户对象
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 确保上传目录存在，权限正确
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 路由定义
@app.route('/')
def index():
    return render_template('index.html')


# 注册、登录、登出、上传文件
@app.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册路由"""
    # 限制已登录用户访问注册页面，直接重定向到仪表板
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    # 实例化注册表单对象
    form = RegisterForm()
    # 验证表单提交是否合法
    if form.validate_on_submit():
        # 创建新的用户对象，将表单数据填充到用户对象中
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        # 设置用户的密码哈希
        user.set_password(form.password.data)
        # 将用户信息保存到数据库中
        db.session.add(user)
        db.session.commit()
        # 注册成功，弹出提示信息，跳转到登录页面
        flash('注册成功，请使用您的账号登录', 'success')
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            print("表单验证失败，错误信息如下：")
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"字段 [{field}]: {error}")

    # 如果是GET请求或验证失败，渲染注册表单页面
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录路由"""
    # 限制已登录用户访问登录页面，直接重定向到仪表板
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    # 实例化登录表单对象
    form = LoginForm()
    # 验证表单提交是否合法
    if form.validate_on_submit():
        # 根据邮箱从数据库中查询用户
        user = User.query.filter_by(email=form.email.data).first()
        # 验证用户是否存在，以及密码是否正确
        if user and user.check_password(form.password.data):
            # 登录用户，设置Flask-Login的用户会话
            login_user(user, remember=form.remember_me.data)
            # 更新用户的最后登录时间
            user.last_login = datetime.utcnow()
            db.session.commit()
            # 跳转到用户之前访问的页面或仪表板页面
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            # 验证失败，弹出错误信息
            flash('登录失败，请检查邮箱和密码是否正确', 'danger')
    # 如果是GET请求或验证失败，渲染登录表单页面
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """用户登出路由"""
    # 清除Flask-Login的用户会话
    logout_user()
    flash('您已成功登出', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """用户后台主页，显示文件上传表单和用户的文件列表"""
    # 实例化上传表单对象
    form = UploadForm()
    # 分页查询当前用户上传的文件列表，按上传时间倒序
    page = request.args.get('page', 1, type=int)
    files = File.query.filter_by(author=current_user)\
        .order_by(File.upload_time.desc())\
        .paginate(page=page, per_page=10)
    return render_template('dashboard.html', form=form, files=files)

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    """处理文件上传请求"""
    form = UploadForm()
    if form.validate_on_submit():
        # 获取上传的文件对象
        file = form.file.data
        # 对文件名进行安全处理，过滤恶意字符
        filename = secure_filename(file.filename)
        # 生成文件的完整存储路径
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # 保存文件到服务器的上传目录
        file.save(save_path)
        # 将文件元数据保存到数据库中
        file_record = File(
            filename=filename,
            filesize=os.path.getsize(save_path),
            author=current_user
        )
        db.session.add(file_record)
        db.session.commit()
        flash(f'文件 {filename} 上传成功！', 'success')
    else:
        # 表单验证失败，回显错误信息
        for error in form.file.errors:
            flash(error, 'danger')
    return redirect(url_for('dashboard'))

@app.route('/download/<int:file_id>')
@login_required
def download_file(file_id):
    """处理文件下载请求，校验文件所属用户是否是当前用户"""
    # 根据文件ID查询文件，或返回404错误
    file_record = File.query.get_or_404(file_id)
    # 权限校验：禁止用户下载其他用户的文件
    if file_record.user_id != current_user.id:
        flash('您没有权限访问该文件', 'danger')
        return redirect(url_for('dashboard'))
    # 从上传目录中下载文件
    return send_from_directory(app.config['UPLOAD_FOLDER'], file_record.filename, as_attachment=True)

@app.route('/delete/<int:file_id>')
@login_required
def delete_file(file_id):
    """处理文件删除请求，校验文件所属用户是否是当前用户"""
    # 根据文件ID查询文件，或返回404错误
    file_record = File.query.get_or_404(file_id)
    # 权限校验：禁止用户删除其他用户的文件
    if file_record.user_id != current_user.id:
        flash('您没有权限删除该文件', 'danger')
        return redirect(url_for('dashboard'))
    # 从数据库中删除文件元数据记录
    db.session.delete(file_record)
    db.session.commit()
    # 从服务器的上传目录中删除实际的文件
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_record.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    flash(f'文件 {file_record.filename} 删除成功！', 'success')
    return redirect(url_for('dashboard'))

@app.route('/about')
def about():
    return render_template('about.html')