from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


app = FastAPI()

# 仅需定义一次模型，所有校验规则声明在模型中
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2)
    price: float = Field(..., gt=0)
    category: str = Field(...)
    stock: int = Field(default=0, ge=0)

@app.post("/products", summary="新增商品")
def create_product(product: Annotated[ProductCreate, Body(embed=True)]):
    # 无任何手动校验逻辑，直接使用校验后的模型数据
    return {"id": 1001, **product.model_dump()}