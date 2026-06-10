from flask import Flask, request, jsonify, abort

# 初始化Flask应用，__name__指定当前模块路径
app = Flask(__name__)
# app.config["JSON_AS_ASCII"] = False
app.json.ensure_ascii = False

# 路径参数语法：<转换器:参数名>，转换器可选int/str/float/path/uuid
@app.route('/get/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # 路径参数直接作为视图函数的参数接收
    return jsonify({
        "code": 200,
        "msg": "success",
        "data": {"user_id": user_id, "username": "zhangsan"}
    })

@app.route('/get/user/list', methods=['GET'])
def get_user_list():
    # request.args：类字典对象，获取URL中的查询参数
    # get(key, default, type)：安全获取参数，不存在时返回默认值，自动转换类型
    page = request.args.get('page', default=1, type=int)
    size = request.args.get('size', default=10, type=int)
    keyword = request.args.get('keyword', default='', type=str)

    return jsonify({
        "code": 200,
        "msg": "success",
        "data": {
            "page": page,
            "size": size,
            "keyword": keyword,
            "list": [{"user_id": 1001, "username": "zhangsan"}]
        }
    })

@app.route('/get/user/token', methods=['GET'])
def get_user_by_token():
    # request.headers：类字典对象，获取所有请求头参数
    token = request.headers.get('Token')
    version = request.headers.get('Version', default='1.0.0')
    return jsonify({
        "code": 200,
        "msg": "success",
        "data": {"token": token, "version": version}
    })

@app.route('/post/user/form', methods=['POST'])
def create_user_by_form():
    # request.form：类字典对象，获取表单格式的请求参数
    username = request.form.get('username')
    age = request.form.get('age', type=int)
    email = request.form.get('email')
    return jsonify({
        "code": 200,
        "msg": "success",
        "data": {"username": username, "age": age, "email": email}
    })

@app.route('/post/user/json', methods=['POST'])
def create_user_by_json():
    # 先校验请求头的Content-Type是否为application/json
    if not request.is_json:
        return jsonify({"code": 400, "msg": "请求格式必须为JSON"}), 400
    # request.get_json()：解析请求体为Python字典
    data = request.get_json()
    # 从字典中提取参数
    username = data.get('username')
    age = data.get('age')
    email = data.get('email')
    return jsonify({
        "code": 200,
        "msg": "success",
        "data": {"username": username, "age": age, "email": email}
    })

@app.route('/post/file/upload', methods=['POST'])
def upload_file():
    # request.files：类字典对象，获取上传的文件对象
    # file 是前端<input type="file" name="file">的name属性值
    file = request.files.get('file')
    if not file:
        return jsonify({"code": 400, "msg": "未选择上传文件"}), 400
    # 获取原始文件名，建议生产环境重命名为随机字符串，避免文件名冲突
    filename = file.filename
    # 保存文件到本地（需提前创建uploads文件夹）
    file.save(f"./uploads/{filename}")
    return jsonify({
        "code": 200,
        "msg": "文件上传成功",
        "data": {"filename": filename}
    })

import re
@app.route('/post/user/validate', methods=['POST'])
def create_user_validate():
    # 1. 校验请求格式是否为JSON
    if not request.is_json:
        return jsonify({"code": 400, "msg": "请求格式必须为JSON"}), 400
    data = request.get_json()
    # 2. 校验必填参数是否存在（all()判断所有元素是否为True）
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    if not all([username, password, email]):
        return jsonify({"code": 400, "msg": "username、password、email为必填参数"}), 400
    # 3. 校验参数类型是否符合预期
    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify({"code": 400, "msg": "username、password必须为字符串类型"}), 400
    if not isinstance(email, str):
        return jsonify({"code": 400, "msg": "email必须为字符串类型"}), 400
    # 4. 校验参数格式（正则校验邮箱格式）
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$'
    if not re.match(email_pattern, email):
        return jsonify({"code": 400, "msg": "邮箱格式不正确"}), 400
    # 5. 校验参数长度（密码6-16位）
    if len(password) < 6 or len(password) > 16:
        return jsonify({"code": 400, "msg": "密码长度必须在6-16位之间"}), 400
    # 校验通过，执行业务逻辑（如存入数据库）
    return jsonify({
        "code": 200,
        "msg": "参数校验成功",
        "data": {"username": username, "email": email}
    })

from marshmallow import Schema, fields, validate, ValidationError
# 1. 定义校验规则Schema，复用性强
class UserSchema(Schema):
    # 字符串类型，必填，长度2-20位
    username = fields.Str(required=True, validate=[validate.Length(min=2, max=20)])
    # 字符串类型，必填，长度6-16位
    password = fields.Str(required=True, validate=[validate.Length(min=6, max=16)])
    # 邮箱格式，必填，自动校验邮箱格式
    email = fields.Email(required=True)
    # 整数类型，可选，范围0-120
    age = fields.Int(required=False, validate=[validate.Range(min=0, max=120)])
# 2. 接口中使用Schema校验参数
@app.route('/post/user/schema', methods=['POST'])
def create_user_schema():
    data = request.get_json()
    user_schema = UserSchema()
    try:
        # load()方法校验参数，返回校验后的参数字典
        valid_data = user_schema.load(data)
    except ValidationError as err:
        # 校验失败，返回标准化错误信息
        return jsonify({"code": 400, "msg": "参数校验失败", "data": err.messages}), 400
    # 校验通过，执行业务逻辑
    return jsonify({
        "code": 200,
        "msg": "参数校验成功",
        "data": valid_data
    })

from flask import abort

@app.route('/get/user/abort/<int:user_id>', methods=['GET'])
def get_user_abort(user_id):
    if user_id > 1000:
        # 手动抛出404异常，第二个参数传递错误描述
        abort(404, description="用户不存在")
    return jsonify({"code": 200, "msg": "success", "data": {"user_id": user_id}})

from flask import jsonify

# 处理404资源不存在异常
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        "code": 404,
        "msg": "资源不存在",
        "data": str(error)
    }), 404

# 处理405请求方法不允许异常
@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({
        "code": 405,
        "msg": "请求方法不允许",
        "data": str(error)
    }), 405

# 处理400参数错误异常
@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({
        "code": 400,
        "msg": "参数错误",
        "data": str(error)
    }), 400

# 处理500服务器内部异常
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "code": 500,
        "msg": "服务器内部异常",
        "data": str(error)
    }), 500

# 捕获所有其他未处理异常，统一返回
@app.errorhandler(Exception)
def unhandled_exception(error):
    return jsonify({
        "code": 500,
        "msg": "服务器未知异常",
        "data": str(error)
    }), 500

# 统一入口：启动开发服务器
if __name__ == '__main__':
    # debug=True 开启热重载，代码修改后自动生效，开发环境必备
    app.run(debug=True, host='0.0.0.0', port=5000)