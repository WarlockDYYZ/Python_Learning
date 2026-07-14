import redis
import json
from celery import Celery


# 初始化Redis连接，用于消费Stream队列
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
# 初始化Celery，将Redis作为消息中间件
celery = Celery('tasks', broker='redis://localhost:6379/0')

# 消费者任务配置，使用Celery定时轮询队列
@celery.task
def consume_order_queue():
    # 1. 确保消费组存在，创建时指定从队列开头消费
    try:
        redis_client.xgroup_create(
            name="stream:order:create",  # Stream队列名称
            groupname="order_process_group",  # 消费组名称
            id="0",  # 从队列开头开始消费
            mkstream=True  # 如果队列不存在则自动创建
        )
    except redis.exceptions.ResponseError:
        # 消费组已存在，忽略异常
        pass

    # 2. 从消费组拉取新消息，阻塞等待
    messages = redis_client.xreadgroup(
        groupname="order_process_group",  # 消费组名称
        consumername="consumer_1",  # 消费者进程标识
        streams={"stream:order:create": ">"},  # > 表示只消费未分配的新消息
        count=1,  # 每次拉取1条消息
        block=5000  # 阻塞等待5秒
    )

    if not messages:
        return "No new messages"

    # 3. 处理消息，完成业务逻辑
    for stream_name, msg_list in messages:
        for msg_id, msg_data in msg_list:
            try:
                # 模拟订单处理业务逻辑
                print(f"Processing order {msg_data['order_id']}")
                # 处理完成后，发送XACK命令确认消息
                redis_client.xack("stream:order:create", "order_process_group", msg_id)
            except Exception as e:
                # 业务处理异常，消息会自动重新入队，等待下次消费
                print(f"Process error: {e}")
                raise

if __name__ == "__main__":
    # 启动消费者，持续监听队列
    consume_order_queue.delay()