from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Optional
try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


app = FastAPI()

# 定义商品请求体模型
class ProductCreate(BaseModel):
    # Field用于添加字段约束，第一个参数...表示必选字段
    name: str = Field(..., min_length=2, max_length=50, description="商品名称，2-50个字符")
    price: float = Field(..., gt=0, description="商品价格，必须大于0")
    category: str = Field(..., description="商品分类，如电子设备、服装等")
    stock: int = Field(default=0, ge=0, description="商品库存，不能为负数")
    description: Optional[str] = Field(None, max_length=200, description="商品简短描述，最多200个字符")
    is_on_sale: bool = Field(default=False, description="是否处于促销状态")

# POST请求：接收JSON格式的请求体
@app.post("/products/", summary="新增商品", status_code=201)
def create_product(product: Annotated[ProductCreate, Body(embed=True)]):
    """
    添加新商品到商品库
    - 必须提交商品名称、价格、分类等核心字段
    - 库存字段不传时默认为0，促销状态默认为false
    """
    # 直接通过product.xxx获取校验后的字段值，无需手动解析
    return {
        "id": 1001,
        "name": product.name,
        "price": product.price,
        "category": product.category,
        "stock": product.stock,
        "description": product.description
    }