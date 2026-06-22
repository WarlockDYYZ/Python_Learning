from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field, EmailStr
from utils.common import register_exception_handlers
from utils.response import success_response

app = FastAPI(title="统一响应示例API")
# 注册全局异常处理器
register_exception_handlers(app)


# 定义请求/响应模型
class UserCreate(BaseModel):
    username: str = Field(..., min_length=2)
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str


# 新增用户接口：使用统一成功响应
@app.post("/users/", response_model=UserResponse, summary="创建用户")
def create_user(user: UserCreate):
    # 模拟业务逻辑：校验用户名是否重复
    if user.username == "admin":
        # 主动抛出异常，被全局异常处理器捕获，返回标准化错误响应
        raise HTTPException(status_code=400, detail="用户名已存在")

    # 模拟创建用户成功，返回标准化成功响应
    db_user = {"id": 1, "username": user.username, "email": user.email}
    return success_response(message="用户创建成功", data=db_user)


# 查询用户接口：返回统一响应格式
@app.get("/users/{user_id}", response_model=UserResponse, summary="根据ID查询用户")
def get_user(user_id: int):
    if user_id > 100:
        raise HTTPException(status_code=404, detail="用户不存在")
    db_user = {"id": user_id, "username": f"user_{user_id}", "email": f"user_{user_id}@example.com"}
    return success_response(message="查询用户成功", data=db_user)