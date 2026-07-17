from contextlib import asynccontextmanager
from fastapi import FastAPI
from redis import asyncio as aioredis, ResponseError
from redis.asyncio import ConnectionPool, Redis
import asyncio
import uuid  # 1. 引入 uuid 用于生成动态消费者名称


# 定义常量，方便全局修改
STREAM_NAME = "stream:order:create"
GROUP_NAME = "order_process_group"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    print("🚀 应用启动中...正在初始化 Redis 消费者")

    app.state.redis_pool = ConnectionPool(
        host="localhost", port=6379, db=0,
        password=None, max_connections=20,
        decode_responses=True, socket_keepalive=True
    )

    redis_client = Redis(connection_pool=app.state.redis_pool)
    consumer_task = asyncio.create_task(consume_order_stream(redis_client))

    yield  # 应用就绪

    print("🛑 应用关闭中...正在停止 Redis 消费者")
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        print("✅ 消费者任务已安全停止")
    finally:
        await app.state.redis_pool.aclose()
        print("✅ Redis 连接池已关闭")


app = FastAPI(title="FastAPI Redis Stream Demo", lifespan=lifespan)


async def consume_order_stream(redis: aioredis.Redis):
    """持续消费订单创建队列的消息，异步处理业务"""

    # 1. 确保消费组存在
    try:
        await redis.xgroup_create(
            name=STREAM_NAME,
            groupname=GROUP_NAME,
            id="0",
            mkstream=True
        )
    except ResponseError as e:
        if "BUSYGROUP" not in str(e):
            raise
        print("ℹ️ 消费组已存在，继续运行...")

    # 2. 【优化点1】生成动态消费者名称，支持多实例部署
    consumer_name = f"consumer_{uuid.uuid4().hex[:8]}"
    print(f"👤 当前消费者身份: {consumer_name}")

    while True:
        try:
            # 3. 【优化点2】先处理 PEL 中的孤儿消息（id="0"）
            # 每次循环先检查是否有其他崩溃消费者遗留的未 ACK 消息
            pending_messages = await redis.xreadgroup(
                groupname=GROUP_NAME,
                consumername=consumer_name,
                streams={STREAM_NAME: "0"},  # 关键："0" 表示拉取 PEL 中的历史消息
                count=1,
                block=0  # 处理孤儿消息不需要阻塞，没有就立即返回
            )

            # 如果有孤儿消息，优先处理
            if pending_messages:
                for stream_name, msg_list in pending_messages:
                    for msg_id, msg_data in msg_list:
                        await process_message(redis, msg_id, msg_data)
                continue  # 处理完孤儿消息后，进入下一轮循环继续检查

            # 4. 如果没有孤儿消息，再去拉取新消息（id=">"）
            new_messages = await redis.xreadgroup(
                groupname=GROUP_NAME,
                consumername=consumer_name,
                streams={STREAM_NAME: ">"},
                count=1,
                block=5000  # 长轮询等待新消息
            )

            if not new_messages:
                continue

            for stream_name, msg_list in new_messages:
                for msg_id, msg_data in msg_list:
                    await process_message(redis, msg_id, msg_data)

        except asyncio.CancelledError:
            print("🛑 收到取消信号，消费者准备退出")
            break
        except Exception as e:
            print(f"❌ Stream 消费主循环异常: {e}")
            await asyncio.sleep(1)


# 5. 【代码重构】将消息处理逻辑抽离为独立函数，避免重复代码
async def process_message(redis: aioredis.Redis, msg_id: str, msg_data: dict):
    """处理单条消息并发送 ACK"""
    try:
        # 注意：如果 ConnectionPool 设置了 decode_responses=True，
        # 这里的 key 可能是字符串 'order_id'，具体取决于你的 redis-py 版本。
        # 建议兼容处理：
        order_id = msg_data.get('order_id') or msg_data.get(b'order_id')
        print(f"📦 Processing order: {order_id} (Msg ID: {msg_id})")

        # TODO: 在这里执行核心业务逻辑...

        # 业务处理成功后，发送 XACK 确认消息
        await redis.xack(STREAM_NAME, GROUP_NAME, msg_id)
    except Exception as e:
        print(f"❌ 订单处理异常 (Msg ID: {msg_id}): {e}")
        # 注意：这里不发送 XACK，消息会留在 PEL 中，等待后续重试