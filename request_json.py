from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/api/login', methods=['POST'])
def api_login():
    # 先判断请求体是否为JSON格式
    if not request.is_json:
        return jsonify({"error": "请求必须是JSON格式"}), 400
    # 解析JSON数据，转换为Python字典
    data = request.get_json()
    # 从字典中获取参数
    username = data.get('username')
    password = data.get('password')
    # 验证逻辑
    if not username or not password:
        return jsonify({"error": "用户名和密码不能为空"}), 400
    if username == 'admin' and password == 'secret':
        # 验证成功，返回JSON格式的响应
        return jsonify({"message": "登录成功", "username": username}), 200
    else:
        return jsonify({"error": "用户名或密码错误"}), 401