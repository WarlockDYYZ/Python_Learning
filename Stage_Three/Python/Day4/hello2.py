from flask import Flask, render_template
app = Flask(__name__)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    # 向模板中传递person变量，其值为路由参数name
    return render_template('hello.html', person=name)