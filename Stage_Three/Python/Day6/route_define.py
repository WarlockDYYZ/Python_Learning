from flask import Flask, request
'''
app = Flask(__name__)

# 需通过methods参数声明HTTP方法，默认仅支持GET
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    return {"user_id": user_id}
# http://127.0.0.1:5000/users/1004
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    return {"username": data.get("username")}


if __name__ == '__main__':
    app.run(debug=True)
'''

from fastapi import FastAPI


# 初始化FastAPI应用，可配置文档标题/版本等元数据
app = FastAPI(title="路由学习Demo", version="1.0")

# -------------------- 用户管理路由 --------------------
# 查询用户：显式声明GET方法，路径参数嵌入URL
@app.get("/users/{user_id}", summary="根据ID获取用户信息", tags=["用户管理"])
def get_user(user_id: int):
    """
    根据用户ID获取详细信息
    - **user_id**: 要查询的用户ID（正整数）
    """
    return {"user_id": user_id, "username": f"user_{user_id}"}

# 新增用户：显式声明POST方法
@app.post("/users", summary="新增用户", tags=["用户管理"])
def create_user(username: str, email: str):
    return {"username": username, "email": email}

# 更新用户：显式声明PUT方法
@app.put("/users/{user_id}", summary="更新用户信息", tags=["用户管理"])
def update_user(user_id: int, username: str):
    return {"user_id": user_id, "new_username": username}

# 删除用户：显式声明DELETE方法
@app.delete("/users/{user_id}", summary="删除用户", tags=["用户管理"])
def delete_user(user_id: int):
    return {"message": f"用户{user_id}删除成功"}
