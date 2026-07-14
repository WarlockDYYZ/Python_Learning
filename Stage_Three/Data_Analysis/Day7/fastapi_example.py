from fastapi import FastAPI, Depends, HTTPException
from redis import asyncio as aioredis, asyncio
import json
from typing import Optional


# 1. 初始化Redis异步连接池
async def get_redis() -> aioredis.Redis:
    pool = aioredis.ConnectionPool(
        host="localhost", port=6379, db=0,
        max_connections=20,  # 连接池最大连接数
        decode_responses=True,  # 自动解码字节结果为字符串
        socket_keepalive=True  # 开启TCP探活，避免负载均衡后的空闲连接被异常关闭
    )
    return aioredis.Redis(connection_pool=pool)

app = FastAPI(title="FastAPI Redis Cache Demo")

# 2. 封装统一缓存读写模板
async def get_or_set_cache(
    key: str, expire: int, redis: aioredis.Redis, func
) -> dict:
    """
    缓存读取模板：存在则直接返回，不存在则执行func查询数据源并缓存
    :param key: Redis缓存键名
    :param expire: 缓存过期时间，单位秒
    :param redis: 异步Redis客户端连接
    :param func: 回调函数，用于查询真实数据源
    """
    cached_data = await redis.get(key)
    if cached_data:
        # 缓存命中，直接反序列化结果
        return json.loads(cached_data)
    # 缓存未命中，执行回调函数查询数据源
    db_data = await func()
    if not db_data:
        raise HTTPException(status_code=404, detail="Data not found")
    # 将查询结果序列化为JSON字符串，写入Redis缓存
    await redis.set(key, json.dumps(db_data, ensure_ascii=False), ex=expire)
    return db_data

# 模拟一个耗时的数据库查询操作
async def query_product_from_db(product_id: int):
    await asyncio.sleep(0.1)
    return {"id": product_id, "name": "无线蓝牙耳机"}

# 3. 业务接口应用缓存逻辑
@app.get("/product/{product_id}", summary="获取商品详情")
async def get_product(
    product_id: int,
    redis: aioredis.Redis = Depends(get_redis)
):
    # 构造规范化的缓存键名
    cache_key = f"product:info:{product_id}"
    # 调用缓存模板方法，设置缓存过期时间为1小时
    return await get_or_set_cache(
        key=cache_key, expire=3600, redis=redis,
        func=lambda: query_product_from_db(product_id)  # 异步数据库查询
    )