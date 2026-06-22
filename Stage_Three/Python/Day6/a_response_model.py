from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional


app = FastAPI()


# -------------------------- 请求体模型 --------------------------
class UserCreate(BaseModel):
    username: str = Field(..., min_length=2)
    email: str = Field(...)
    password: str = Field(..., min_length=8)  # 密码仅在请求体中接收，不返回响应
    nickname: Optional[str] = Field(None, description="用户昵称")


# -------------------------- 响应体模型 --------------------------
class UserResponse(BaseModel):
    id: int = Field(..., description="用户唯一ID")
    username: str = Field(..., description="用户名")
    email: str = Field(..., description="用户邮箱")
    nickname: Optional[str] = Field(None, description="用户昵称")
    # 响应模型中明确不包含password字段，避免泄露敏感信息


# -------------------------- 使用响应模型的接口 --------------------------
@app.post("/users/", response_model=UserResponse, status_code=201, summary="创建用户")
def create_user(user: UserCreate):
    """
    创建新用户，返回用户基础信息
    响应中自动过滤密码等敏感字段
    """
    # 模拟业务逻辑：创建用户，生成用户ID
    db_user = {
        "id": 1,
        "username": user.username,
        "email": user.email,
        "nickname": user.nickname
    }
    # 直接返回字典，FastAPI自动按照response_model过滤、序列化字段
    return db_user