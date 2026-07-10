import redis


r = redis.Redis(decode_responses=True)

# 1. 插入元素：从表头/表尾插入，支持批量插入
r.lpush("order:create:queue", "order:1001")  # 表头左插
r.rpush("order:create:queue", "order:1002")  # 表尾右插
r.lpush("order:create:queue", "order:1003", "order:1004")  # 批量左插

# 2. 弹出元素：原子性移除并返回表头/表尾元素
order_id = r.lpop("order:create:queue")  # 弹出表头元素
order_id = r.rpop("order:create:queue")  # 弹出表尾元素

# 3. 阻塞式弹出：没有元素时阻塞等待，超时后返回None
order_id = r.blpop("order:create:queue", timeout=5)  # 阻塞5秒，返回键名和元素值
order_id = r.brpop("order:create:queue", timeout=5)  # 阻塞式弹出表尾元素

# 4. 弹出并插入另一个队列：原子性操作，安全迁移任务
r.rpoplpush("order:create:queue", "order:process:queue")  # 弹出原队列表尾元素，插入到新队列表头

# 5. 获取队列指定范围内的元素，支持分页查询
elements = r.lrange("order:create:queue", 0, -1)  # 获取所有元素，索引从0开始，-1表示最后一个元素
length = r.llen("order:create:queue")  # 获取队列当前元素数量