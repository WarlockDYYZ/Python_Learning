from flask import Flask
app = Flask(__name__)

# 规范 URL 末尾带斜杠
@app.route('/projects/')
def projects():
    return 'The project page'

# 规范 URL 末尾不带斜杠
@app.route('/about')
def about():
    return 'The about page'