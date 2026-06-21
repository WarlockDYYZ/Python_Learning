from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import List, Optional
try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


app = FastAPI()

# -------------------------- 嵌套子模型：地址信息 --------------------------
class Address(BaseModel):
    province: str = Field(..., min_length=2, max_length=30, description="省份名称")
    city: str = Field(..., min_length=2, max_length=30, description="城市名称")
    detail: str = Field(..., min_length=5, max_length=100, description="详细街道门牌号")
    zip_code: Optional[str] = Field(None, pattern=r'^\d{6}$', description="6位邮政编码")
    phone: Optional[str] = Field(None, pattern=r'^\d{11}$', description="收货人11位手机号码")

# -------------------------- 主模型：带地址的用户信息 --------------------------
class UserCreate(BaseModel):
    username: str = Field(..., min_length=2, max_length=20, description="用户名")
    email: str = Field(..., pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', description="有效邮箱地址")
    password: str = Field(..., min_length=8, description="登录密码，至少8位")
    nickname: Optional[str] = Field(None, max_length=30, description="用户昵称")
    # 嵌套Address模型：用户的收货地址列表
    addresses: List[Address] = Field(..., min_length=1, description="用户收货地址列表，至少填写一个地址")

# -------------------------- 使用嵌套模型的接口 --------------------------
@app.post("/users/with-address", summary="创建带地址信息的用户")
def create_user_with_address(user: Annotated[UserCreate, Body(embed=True)]):
    """
    创建包含收货地址列表的完整用户信息
    请求体中必须包含用户基础信息，以及至少一个收货地址的完整结构化数据
    """
    # 直接获取嵌套模型的字段值
    first_address = user.addresses[0]
    return {
        "id": 1,
        "username": user.username,
        "email": user.email,
        "first_address": f"{first_address.province}{first_address.city}{first_address.detail}",
        "address_count": len(user.addresses)
    }