import os
from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
# 配置文件上传后的存储路径
app.config['UPLOAD_FOLDER'] = 'uploads'
# 配置允许上传的文件扩展名集合
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
# 配置上传文件的最大尺寸，限制为16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# 检查上传的文件扩展名是否符合允许的范围
def allowed_file(filename):
    # 检查文件名中是否包含扩展名，以及扩展名是否在允许列表中
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 检查请求中是否包含文件部分
        if 'file' not in request.files:
            flash('没有选择任何文件', 'error')
            return redirect(request.url)
        # 获取上传的文件对象
        file = request.files['file']
        # 检查用户是否选择了文件
        if file.filename == '':
            flash('未选择需要上传的文件', 'error')
            return redirect(request.url)
        # 验证文件类型和文件名是否合法
        if file and allowed_file(file.filename):
            # 对文件名进行安全处理，移除可能包含恶意路径的字符
            filename = secure_filename(file.filename)
            # 拼接文件的完整存储路径
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # 保存文件到服务器的指定目录
            file.save(save_path)
            flash(f'文件 {filename} 上传成功！', 'success')
            return redirect(url_for('uploaded_file', filename=filename))
        else:
            flash('不允许上传该类型文件，请检查文件扩展名', 'error')
            return redirect(request.url)
    # GET请求默认返回上传文件表单页面
    return render_template('upload.html')

@app.route('/files/<filename>')
def uploaded_file(filename):
    # 这里简单返回一个消息，实际项目中可以返回 render_template 渲染一个展示图片的页面
    return f'你上传的文件是: {filename}'