from flask import Flask
from werkzeug.routing import BaseConverter

class RegexConverter(BaseConverter):
    """正则表达式转换器，允许使用正则约束路由参数"""
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        # 将传入的第一个参数保存为正则匹配规则
        self.regex = items[0]

# 将自定义转换器注册到Flask应用中
app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter

# 使用自定义转换器：约束user_id必须为5-8位的数字
@app.route('/user/<regex("[0-9]{5,8}"):user_id>')
def show_user(user_id):
    return f'User ID: {user_id}'