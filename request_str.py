from flask import Flask, request
app = Flask(__name__)

@app.route('/search')
def search():
    # 获取查询参数q，默认值为空字符串
    query = request.args.get('q', '')
    # 获取查询参数sort，默认值为'recent'
    sort_by = request.args.get('sort', 'recent')
    return f'Searching for: {query} (sort: {sort_by})'