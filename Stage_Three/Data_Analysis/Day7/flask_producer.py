from fastapi import FastAPI, Depends
from redis import asyncio as aioredis


app = FastAPI(title="FastAPI Redis Stream Producer Demo")

# 复用之前的异步Redis连接池
async def get_redis() -> aioredis.Redis:
    pool = aioredis.ConnectionPool(
        host="localhost", port=6379, db=0, max_connections=20, decode_responses=True
    )
    return aioredis.Redis(connection_pool=pool)

# 模拟数据库订单创建操作
async def create_order_in_db(order_data: dict):
    # 实际业务中会执行数据库插入操作
    return {"order_id": order_data["order_id"], "status": "created"}

# 业务接口：创建订单，将任务写入Stream队列
@app.post("/order", summary="创建订单")
async def create_order(
    order_data: dict,
    redis: aioredis.Redis = Depends(get_redis)
):
    # 1. 先执行核心的数据库操作，保障订单落地
    await create_order_in_db(order_data)
    # 2. 将非核心的后续任务投递到Redis Stream队列
    # 使用XADD命令插入消息，*表示自动生成唯一消息ID
    msg_id = await redis.xadd(
        name="stream:order:create",  # Stream队列名称
        fields={
            "order_id": order_data["order_id"],
            "user_id": order_data["user_id"],
            "amount": order_data["amount"],
            "timestamp": order_data["timestamp"]
        },
        id="*",  # 自动生成毫秒级时间戳+序号的唯一ID
        maxlen=10000,  # 限制队列最大长度，避免内存无限增长
        approximate=True
    )
    return {"status": "success", "message": "Order created", "msg_id": msg_id}