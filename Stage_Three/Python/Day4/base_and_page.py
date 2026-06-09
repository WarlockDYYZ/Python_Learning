from flask import Flask, render_template

app = Flask(__name__)

# 1. 首页路由：必须渲染子模板 page.html，而不是 base.html
@app.route('/')
def index():
    # 传递 items 数据给子模板
    return render_template('page.html', items=[{'name': '测试数据1'}, {'name': '测试数据2'}])

# 2. 页面路由：同样渲染子模板
@app.route('/page')
def page():
    return render_template('page.html', items=[{'name': '测试数据1'}, {'name': '测试数据2'}])

@app.route('/login')
def login():
    return 'login'

@app.route('/logout')
def logout():
    return 'logout'

@app.route('/about')
def about():
    return 'about'

@app.route('/dashboard')
def dashboard():
    return 'dashboard'

if __name__ == '__main__':
    # 3. 务必开启 debug 模式，以便在浏览器直接看到真实的报错原因
    app.run(debug=True)