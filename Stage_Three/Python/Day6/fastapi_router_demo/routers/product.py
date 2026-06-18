from fastapi import APIRouter, Query, status
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi import HTTPException


# 创建商品路由实例
product_router = APIRouter(
    prefix="/api/products",
    tags=["商品管理"],
    responses={404: {"description": "商品不存在"}},
)


# 商品请求体模型
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="商品名称，2-50个字符")
    price: float = Field(..., gt=0, description="商品价格，必须大于0")
    category: str = Field(..., description="商品分类")
    stock: int = Field(default=0, ge=0, description="商品库存，不能为负数")
    description: Optional[str] = Field(None, max_length=200, description="商品简短描述")


# -------------------- 商品接口 --------------------
@product_router.post("/", summary="新增商品", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    """添加新商品到商品库，需提交商品名称、价格、分类等核心信息"""

    return {"id": 1001, **product.model_dump()}

@product_router.get("/", summary="分页查询商品列表")
def list_products(
        page: int = Query(1, ge=1, description="页码，从1开始"),
        page_size: int = Query(10, ge=1, le=100, description="每页条数，最大100"),
        category: Optional[str] = Query(None, description="商品分类筛选，不填写则查询全部分类")
):
    """分页查询商品列表，支持按分类筛选数据"""

    # 模拟业务逻辑：根据分页参数和筛选条件从数据库查询
    return {
        "data": [{"id": 1001, "name": "测试商品", "price": 99.9}],
        "total": 100,
        "page": page,
        "page_size": page_size
    }

@product_router.get("/{product_id}", summary="根据ID查询商品详情")
def get_product(product_id: int):
    """根据商品ID查询商品完整详情，ID为正整数"""
    if product_id > 10000:
        raise HTTPException(status_code=404, detail="商品不存在")

    return {"id": product_id, "name": "测试商品", "price": 99.9, "stock": 100}

@product_router.put("/{product_id}", summary="更新商品信息")
def update_product(product_id: int, product: ProductCreate):
    """更新指定ID的商品完整信息，需提交全部必填字段"""
    if product_id > 10000:
        raise HTTPException(status_code=404, detail="商品不存在")

    return {"id": product_id, **product.model_dump()}

@product_router.delete("/{product_id}", summary="删除商品", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    """根据商品ID删除对应商品，删除后数据不可恢复"""
    if product_id > 10000:
        raise HTTPException(status_code=404, detail="商品不存在")

    # 204 状态码表示服务器成功处理了请求，但不需要返回任何消息体（Body）。
    # 因此这里直接 return，不要返回字典或字符串。
    return