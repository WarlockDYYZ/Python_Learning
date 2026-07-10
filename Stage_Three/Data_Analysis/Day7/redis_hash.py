import redis


r = redis.Redis(decode_responses=True)

# 1. 单个字段设置/获取：原子性更新指定字段
r.hset("product:1001:info", "name", "无线蓝牙耳机")
r.hset("product:1001:info", "stock", "100")
product_name = r.hget("product:1001:info", "name")  # 读取单个字段值

# 2. 批量字段设置/获取：减少网络往返开销
r.hmset("product:1001:info", {"price": "299", "sales": "500"})  # 批量设置字段
product_info = r.hmget("product:1001:info", ["name", "stock", "price"])  # 批量获取字段值

# 3. 获取Hash中所有字段和值（慎用于超大数据量，会阻塞Redis）
all_fields = r.hgetall("product:1001:info")  # 返回dict类型的完整字段映射

# 4. 原子性增加哈希字段的数值：等价于HINCRBY命令
r.hincrby("product:1001:info", "sales", 1)  # 商品销量+1
r.hincrbyfloat("product:1001:info", "price", -10.5)  # 商品价格减10.5元

# 5. 删除指定字段：HDEL命令，支持批量删除
r.hdel("product:1001:info", "stock")  # 删除stock字段，返回删除成功的数量