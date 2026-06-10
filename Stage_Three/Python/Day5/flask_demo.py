from flask import Flask, request, jsonify, abort

# 初始化Flask应用，__name__指定当前模块路径
app = Flask(__name__)

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

# 统一入口：启动开发服务器
if __name__ == '__main__':
    # debug=True 开启热重载，代码修改后自动生效，开发环境必备
    app.run(debug=True, host='0.0.0.0', port=5000)