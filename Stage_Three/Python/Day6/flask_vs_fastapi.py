from flask import Flask, request, jsonify


app = Flask(__name__)

# flask 手动校验
# @app.get("/users")  # 这是 FastAPI 的写法
@app.route("/users", methods=["GET"])
def get_users():
    # 手动提取查询参数
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 10, type=int)

    # 手动编写校验逻辑
    if page < 1:
        return jsonify({"error": "page必须大于等于1"}), 400
    if page_size < 1 or page_size > 100:
        return jsonify({"error": "page_size必须在1-100之间"}), 400

    return {"page": page, "page_size": page_size}
# flask --app flask_vs_fastapi run
# http://127.0.0.1:5000/users
# http://127.0.0.1:5000/users?page=2&page_size=20
# 访问的路由中可以加上 "/"，此时就访问 users?... users/?...，都可以


# fastapi 自动校验
from fastapi import FastAPI, Query
from typing import Annotated
app = FastAPI()
@app.get("/users")
def get_users(
        page: Annotated[int, Query(ge=1, description="页码，从1开始")] = 1,
        page_size: Annotated[int, Query(ge=1, le=100, description="每页条数，最大100")] = 10
):
    # 无需任何手动校验，FastAPI自动完成所有规则校验
    return {"page": page, "page_size": page_size}
# uvicorn flask_vs_fastapi:app --reload
# http://127.0.0.1:8000/users?page=5&page_size=50