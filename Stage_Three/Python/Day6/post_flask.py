from flask import Flask, request, jsonify


app = Flask(__name__)


@app.post("/products")
def create_product():
    # 手动提取JSON请求体，需判断解析是否成功
    data = request.get_json()
    if not data:
        return jsonify({"error": "请求体必须为JSON格式"}), 400

    # 手动校验每个字段的类型和约束
    if not data.get("name") or len(data["name"]) < 2:
        return jsonify({"error": "商品名称长度不能少于2个字符"}), 400
    # 防止字段不存在报错 KeyError，其他字段也可以做类似修改
    price = data.get("price")
    if not isinstance(price, (int, float)) or price <= 0:
        return jsonify({"error": "商品价格必须大于0"}), 400
    if not data.get("category"):
        return jsonify({"error": "商品分类不能为空"}), 400
    if not isinstance(data.get("stock"), int) or data["stock"] < 0:
        return jsonify({"error": "商品库存不能为负数"}), 400

    # 校验通过后，手动提取字段处理业务逻辑
    return {"id": 1001, "name": data["name"], "price": data["price"]}, 201