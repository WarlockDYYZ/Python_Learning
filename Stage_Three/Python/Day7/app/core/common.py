# app/core/common.py
from fastapi import Depends, Query, HTTPException
from typing import Annotated, Optional, Any


# 公共分页参数依赖：统一校验分页逻辑，设置默认值
async def get_pagination_params(
    page: int = Query(1, ge=1, description="页码，从1开始"),
    page_size: int = Query(10, ge=1, le=100, description="每页条数，最大100")
) -> dict[str, int]:
    return {"page": page, "page_size": page_size}

# 商品筛选参数依赖：统一校验价格区间、分类参数
async def get_product_filter_params(
    category: Optional[str] = Query(None, description="商品分类筛选"),
    min_price: float = Query(0, ge=0, description="最低价格，不能小于0"),
    max_price: float = Query(10000, ge=0, description="最高价格，不能小于0")
) -> dict[str, Any]:
    if min_price > max_price:
        raise HTTPException(status_code=400, detail="最低价格不能高于最高价格")
    return {
        "category": category,
        "min_price": min_price,
        "max_price": max_price
    }

# 类型别名，路由中直接复用
PaginationDep = Annotated[dict[str, int]], Depends(get_pagination_params)
ProductFilterDep = Annotated[dict[str, Any]], Depends(get_product_filter_params)