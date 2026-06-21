from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel, Field
try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


app = FastAPI()

# 定义请求体模型
class ProductUpdate(BaseModel):
    name: str = Field(..., min_length=2)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)

@app.put("/products/{product_id}", summary="更新商品信息")
def update_product(
    # 1. 请求体：商品更新数据
    product: Annotated[ProductUpdate, Body(embed=True)],
    # 2. 路径参数：商品ID
    product_id: Annotated[int, Path(ge=1, description="要更新的商品ID")],
    # 3. 查询参数：是否返回更新后的完整商品信息
    return_full: Annotated[bool, Query(description="是否返回更新后的完整商品详情")] = False
):
    """
    更新指定ID的商品信息
    需提交路径参数（商品ID）、可选查询参数（是否返回完整详情）、JSON格式请求体（更新的商品数据）
    """
    # 模拟业务逻辑：更新数据库中的商品数据
    result = {
        "product_id": product_id,
        "updated_name": product.name,
        "updated_price": product.price,
        "updated_stock": product.stock
    }
    if return_full:
        result["full_product_info"] = {**product.model_dump(), "id": product_id}
    return result