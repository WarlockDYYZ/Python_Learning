from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr


# 创建APIRouter实例：统一前缀为/api/users，文档标签为"用户管理"
user_router = APIRouter(
    prefix="/api/users",  # 该模块所有路由的公共前缀
    tags=["用户管理"],      # 接口文档的分组标签
    responses={404: {"description": "用户不存在"}},  # 统一响应文档配置
)


# 定义请求体模型
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


# -------------------- 用户接口 --------------------
@user_router.post("/", summary="创建新用户", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    """
    注册新用户，提交用户基础信息
    - **username**: 用户名（全局唯一，2-20个字符）
    - **email**: 有效邮箱地址，用于后续身份验证
    - **password**: 登录密码（至少8位，包含字母和数字）
    """
    # 模拟业务逻辑：校验用户是否存在、写入数据库等
    if user.username == "admin":
        raise HTTPException(status_code=400, detail="用户名已被占用")

    return {"id": 1, "username": user.username, "email": user.email}

@user_router.get("/{user_id}", summary="根据ID查询用户")
def get_user(user_id: int):
    """根据用户ID获取用户详情，ID为正整数"""
    if user_id > 100:
        raise HTTPException(status_code=404, detail="用户不存在")

    return {"user_id": user_id, "username": f"user_{user_id}", "role": "normal"}

@user_router.put("/{user_id}", summary="更新用户信息")
def update_user(user_id: int, user: UserCreate):
    """更新指定ID的用户完整信息，需提交全部必填字段"""
    if user_id > 100:
        raise HTTPException(status_code=404, detail="用户不存在")

    return {"user_id": user_id, "updated_username": user.username, "updated_email": user.email}

@user_router.delete("/{user_id}", summary="删除用户")
def delete_user(user_id: int):
    """根据用户ID删除对应用户，删除后数据不可恢复"""
    if user_id > 100:
        raise HTTPException(status_code=404, detail="用户不存在")

    return {"detail": f"用户{user_id}删除成功"}
