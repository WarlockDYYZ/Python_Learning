from flask import Flask, url_for, redirect

app = Flask(__name__)

@app.route('/')
def index():
    # 生成指向about视图的URL
    about_url = url_for('about')
    return f'Index Page <a href="{about_url}">About</a>'

@app.route('/about')
def about():
    return 'About Page'

@app.route('/profile/<username>')
def profile(username):
    return f'Profile: {username}'

# 演示使用url_for生成带查询参数的URL
@app.route('/login')
def login():
    next_url = url_for('index', next='/dashboard')
    return redirect(next_url)