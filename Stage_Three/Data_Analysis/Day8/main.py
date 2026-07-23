# main.py
from fastapi import FastAPI, Depends, Request
from pydantic import BaseModel
from redis import asyncio as aioredis
from utils.redis_decorator import log_redis_operation  # 复用装饰器
import json
from contextlib import asynccontextmanager
import redis


class Product(BaseModel):  # 定义数据模型
    id: int
    name: str
    price: float
    stock: int


app = FastAPI(title="FastAPI Redis Log Demo")

# 全局异步Redis连接池，在应用启动时初始化
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis_pool = aioredis.ConnectionPool(
        host="localhost",
        port=6379,
        password="your-redis-password",
        db=0,
        max_connections=20,
        decode_responses=True
    )
    yield
    await app.state.redis_pool.disconnect()

app.router.lifespan_context = lifespan

# 依赖注入：获取异步Redis连接
async def get_redis_conn(request: Request) -> aioredis.Redis:
    return aioredis.Redis(connection_pool=request.app.state.redis_pool)

# 业务接口示例，自动记录异步Redis操作日志
@app.get("/product/{product_id}")
async def get_product(
    product_id: int,
    redis_conn: aioredis.Redis = Depends(get_redis_conn)
):
    cache_key = f"product:info:{product_id}"
    # 读取缓存，自动记录日志
    try:
        product_data = await get_product_cache(redis_conn, cache_key)
    except redis.RedisError:  # 捕获所有 Redis 异常
        product_data = None  # 降级：跳过缓存
    # 读取缓存时安全处理
    if product_data:
        return {"data": Product.model_validate_json(product_data), "source": "cache"}

    # 缓存未命中，查询数据库
    product = {"id": product_id, "name": "无线蓝牙耳机", "price": 299.99, "stock": 100}
    await set_product_cache(redis_conn, cache_key, product)
    return {"data": product, "source": "database"}

# 复用日志装饰器，适配异步命令
@log_redis_operation(biz_type="product_cache")
async def get_product_cache(redis_conn, cache_key):
    return await redis_conn.get(cache_key)

@log_redis_operation(biz_type="product_cache")
async def set_product_cache(redis_conn, cache_key, product_dict):
    await redis_conn.setex(cache_key, 3600, json.dumps(product_dict, ensure_ascii=False))