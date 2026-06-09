from flask import Flask
app = Flask(__name__)

# 使用path转换器捕获多级分类路径
@app.route('/category/<path:subpath>')
def show_category(subpath):
    return f'Category: {subpath}'

# 使用uuid转换器匹配标准UUID字符串
@app.route('/item/<uuid:item_id>')
def show_item(item_id):
    return f'Item UUID: {item_id}'