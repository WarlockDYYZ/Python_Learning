from fastapi import FastAPI, HTTPException, Path
try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated
from enum import Enum


app = FastAPI()

# 基础用法
# 路径参数user_id，声明为int类型
@app.get("/users/{user_id}")
def get_user(user_id: int):
    """根据用户ID获取信息，ID必须为正整数"""
    return {"user_id": user_id}

# 高级参数校验
@app.get("/users2/{user_id}", summary="获取用户详情")
def get_user(
        user_id: Annotated[
            int,
            Path(
                title="用户ID",
                description="系统内唯一用户ID，必须为正整数，且不超过10000",
                ge=1,  # 约束：大于等于1
                le=10000,  # 约束：小于等于10000
                example=123  # 文档中显示的参数示例值
            )
        ]
    ):
    """根据用户ID获取详细信息"""
    return {"user_id": user_id}


# 定义枚举类，限定参数的可选值
class UserRole(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"

@app.get("/users/role/{role}", summary="按角色查询用户")
def get_users_by_role(role: UserRole):
    """
    根据用户角色批量查询用户列表
    - role: 可选值为admin（管理员）、editor（编辑）、viewer（普通查看者）
    """
    # 枚举值可直接通过role.value获取字符串值
    return {"role": role.value, "users": [{"id": 1, "username": "test_user"}]}

@app.get("/files/{file_path:path}", summary="查询文件路径信息")
def get_file(file_path: str):
    """
    接收包含斜杠的完整文件路径，返回文件存储信息
    - file_path: 项目存储目录下的相对文件路径
    """
    return {"file_path": file_path}








































































































