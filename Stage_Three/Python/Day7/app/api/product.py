# app/api/product.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
import asyncio
from app.core.deps import AsyncSessionDep, HttpClientDep, RedisDep, PaginationDep, ProductFilterDep
from app import crud, schemas
from app.utils.cache import get_cache_key, set_cache_data

router = APIRouter(prefix="/products", tags=["商品管理"])

@router.get("/", response_model=schemas.ProductListResponse, summary="分页查询商品列表")
async def get_products(
    pagination: PaginationDep,  # 注入分页参数
    filter_params: ProductFilterDep,  # 注入商品筛选参数
    db: AsyncSessionDep,  # 注入异步数据库会话
    http_client: HttpClientDep,  # 注入异步HTTP客户端
    redis_client: RedisDep  # 注入异步Redis客户端
):
    """
    分页查询商品列表，支持分类、价格区间筛选；
    优先读取Redis缓存，缓存不存在时异步查询数据库，并发获取第三方库存、价格信息；
    """
    # 1. 从缓存中获取数据（若存在）
    cache_key = get_cache_key(
        "products_list",
        page=pagination["page"],
        page_size=pagination["page_size"],
        **filter_params
    )
    cached_data = await redis_client.get(cache_key)
    if cached_data:
        # 直接返回缓存数据，无需调用数据库/第三方服务，大幅缩短响应时间
        return schemas.ProductListResponse.parse_raw(cached_data)

    # 2. 并发执行数据库查询、商品总数查询，减少串行耗时
    try:
        db_task = crud.product.get_products_paginated(
            db=db,
            skip=(pagination["page"] - 1) * pagination["page_size"],
            limit=pagination["page_size"],
            **filter_params
        )
        count_task = crud.product.count_products(db=db, **filter_params)
        products, total = await asyncio.gather(db_task, count_task)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"商品数据库查询异常：{str(e)}")

    if not products:
        return schemas.ProductListResponse(data=[], total=0, **pagination)

    # 3. 并发调用第三方库存、价格服务，批量获取关联信息
    product_ids = [p.id for p in products]
    try:
        inventory_task = http_client.get("/inventory/batch", params={"product_ids": product_ids})
        price_task = http_client.get("/prices/batch", params={"product_ids": product_ids})
        inventory_res, price_res = await asyncio.gather(inventory_task, price_task)

        # 校验第三方接口响应状态
        inventory_res.raise_for_status()
        price_res.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"库存/价格服务异常：{str(e)}")
    except httpx.TimeoutException:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="库存/价格服务请求超时")

    # 4. 解析第三方响应，聚合完整商品数据
    inventory_map = {item["product_id"]: item["stock_num"] for item in inventory_res.json()}
    price_map = {item["product_id"]: item["price"] for item in price_res.json()}

    product_list = []
    for p in products:
        product_list.append(schemas.ProductResponse(
            id=p.id,
            name=p.name,
            category=p.category,
            price=price_map.get(p.id),
            stock_num=inventory_map.get(p.id),
            description=p.description
        ))

    result = schemas.ProductListResponse(
        data=product_list,
        total=total,
        page=pagination["page"],
        page_size=pagination["page_size"]
    )

    # 5. 将结果写入Redis缓存，有效期5分钟，减轻后续请求压力
    await redis_client.setex(cache_key, 300, result.json())
    return result