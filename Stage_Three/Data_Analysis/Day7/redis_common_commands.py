import redis

# 建立Redis连接，默认连接本地6379端口，自动解码返回的字节结果
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# 1. 基础SET/GET操作：设置键值对，带过期时间的缓存式设置
r.set("product:1001:name", "无线蓝牙耳机", ex=3600)  # 缓存1小时
product_name = r.get("product:1001:name")  # 获取键值，不存在则返回None
print(product_name)

# 2. 批量操作：同时设置/获取多个键值，减少网络往返开销
r.mset({"user:1001:name": "Alice", "user:1001:age": "30"})
user_info = r.mget(["user:1001:name", "user:1001:age"])  # 返回值列表

# 3. 原子自增/自减：无需额外加锁，就能保障并发安全的计数器操作
r.set("product:1001:views", "0")  # 初始化浏览计数器
r.incr("product:1001:views")  # 计数器+1
r.incrby("product:1001:views", 5)  # 计数器+5
r.decr("product:1001:views")  # 计数器-1

# 4. 带条件的SET操作：分布式锁典型实现
r.set("lock:order:1001", "unique_lock_id", nx=True, ex=10)  # 键不存在时设置，过期时间10秒