from flask import Flask
app = Flask(__name__)

# 捕获字符串类型的用户名（默认转换器，不允许包含斜杠）
@app.route('/user/<username>')
def show_user_profile(username):
    return f'User {username}'

# 捕获整数类型的帖子ID，转换器会自动将参数转换为 int 类型
@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Post {post_id}'

# 捕获路径类型的子路径（允许包含斜杠）
@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return f'Subpath {subpath}'

# 捕获 UUID 类型的项目ID，转换器会自动校验并转换为 UUID 对象
@app.route('/item/<uuid:item_id>')
def show_item(item_id):
    return f'Item UUID: {item_id}'