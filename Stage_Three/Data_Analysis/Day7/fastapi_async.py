from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends
from redis.asyncio import ConnectionPool, Redis
from typing import AsyncGenerator

from fastapi import HTTPException
from redis import asyncio as aioredis
import json
from typing import Optional


# 1. 定义 lifespan 上下文管理器，集中管理资源的生命周期
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    FastAPI 生命周期管理
    1. yield 之前：启动逻辑（初始化 Redis 连接池）
    2. yield 之后：关闭逻辑（优雅断开连接池）
    """
    print("应用启动中...正在初始化 Redis 连接池")
    # 初始化全局 Redis 异步连接池，并挂载到 app.state
    app.state.redis_pool = ConnectionPool(
        host="localhost",
        port=6379,
        db=0,
        password=None,
        max_connections=20,
        decode_responses=True,
        socket_keepalive=True
    )

    yield  # 应用进入就绪状态，开始接收请求

    print("应用关闭中...正在清理 Redis 连接池")
    # 应用关闭时，优雅地断开连接池，释放所有连接
    await app.state.redis_pool.disconnect()


# 2. 创建 FastAPI 应用，并注入 lifespan
app = FastAPI(title="FastAPI Redis Demo", lifespan=lifespan)


# 3. 依赖注入：获取异步 Redis 客户端连接
async def get_redis(request: Request) -> AsyncGenerator[Redis, None]:
    # 从全局连接池中获取一个连接
    redis_client = Redis(connection_pool=request.app.state.redis_pool)
    try:
        yield redis_client
    finally:
        # 释放连接，归还到连接池
        await redis_client.aclose()


# 模拟数据库异步查询操作
async def query_product_from_db(product_id: int) -> Optional[dict]:
    """模拟从数据库查询商品详情，耗时0.5秒"""
    import asyncio
    await asyncio.sleep(0.5)
    if product_id <= 0:
        return None
    return {
        "id": product_id,
        "name": f"无线蓝牙耳机{product_id}",
        "price": 299.99,
        "stock": 100
    }


# 缓存穿透与加速
# 业务接口：获取商品详情，添加缓存逻辑
@app.get("/product/{product_id}", summary="获取商品详情（缓存加速）")
async def get_product(
    product_id: int,
    redis: aioredis.Redis = Depends(get_redis)
):
    # 构造规范化的缓存键名
    cache_key = f"product:info:{product_id}"
    # 1. 先读取Redis缓存
    cached_data = await redis.get(cache_key)
    if cached_data:
        # 缓存命中，直接反序列化返回，无需查询数据库
        return {"data": json.loads(cached_data), "source": "cache"}

    # 2. 缓存未命中，查询后端数据库
    db_data = await query_product_from_db(product_id)
    if not db_data:
        raise HTTPException(status_code=404, detail="商品不存在")

    # 3. 将查询结果写入缓存，设置1小时过期时间
    await redis.set(
        cache_key,
        json.dumps(db_data, ensure_ascii=False),
        ex=3600  # 过期时间1小时，自动更新热数据
    )
    return {"data": db_data, "source": "database"}