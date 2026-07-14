from fastapi import FastAPI, Depends
from redis import asyncio as aioredis
from typing import List, Dict


app = FastAPI(title="FastAPI Redis Real-Time Demo")

# 复用异步Redis连接池
async def get_redis() -> aioredis.Redis:
    pool = aioredis.ConnectionPool(
        host="localhost", port=6379, db=0, max_connections=20, decode_responses=True
    )
    return aioredis.Redis(connection_pool=pool)

# 1. 实时曝光/浏览计数接口
@app.post("/product/{product_id}/view", summary="记录商品浏览量")
async def product_view(
    product_id: int,
    redis: aioredis.Redis = Depends(get_redis)
):
    # 原子性增加商品浏览计数，INCRBY命令天然保障并发安全
    await redis.incrby(f"product:counter:{product_id}", 1)
    # 同步更新商品的实时排行榜Sorted Set，得分即为浏览量
    await redis.zadd(
        name="ranking:product:view",
        mapping={str(product_id): 1},
        incr=True
    )
    return {"status": "success", "message": "View recorded"}

# 2. 实时排行榜查询接口
@app.get("/product/ranking", summary="获取商品实时浏览排行榜")
async def get_product_ranking(
    top_n: int = 10,
    redis: aioredis.Redis = Depends(get_redis)
) -> List[Dict]:
    # 从Sorted Set中按分数倒序，获取top_N个商品ID
    product_ids = await redis.zrevrange(
        name="ranking:product:view",  # 排行榜的键名
        start=0,  # 从第一名开始
        end=top_n - 1,  # 取top_N名
        withscores=True  # 同时返回得分
    )
    # 批量获取商品的最新浏览量
    pipe = redis.pipeline()
    for product_id, _ in product_ids:
        # 必须 await，否则命令不会进入管道
        await pipe.hgetall(f"product:info:{product_id}")

        # 最后再统一 await 执行，一次性拿回所有结果
    product_details = await pipe.execute()
    # 聚合商品基础信息和浏览量得分
    ranking_list = []
    for (product_id, score), detail in zip(product_ids, product_details):
        detail["views"] = int(score)
        ranking_list.append(detail)
    return ranking_list