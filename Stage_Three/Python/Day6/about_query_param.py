from fastapi import FastAPI

app = FastAPI()

# 查询参数：page（页码，默认1）、page_size（每页条数，默认10）
@app.get("/users", summary="分页查询用户列表")
def get_users(page: int = 1, page_size: int = 10):
    """分页查询系统内用户列表，支持自定义页码和每页显示条数"""
    return {"page": page, "page_size": page_size, "data": [{"id": 1, "username": "test"}]}

#