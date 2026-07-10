import redis


r = redis.Redis(decode_responses=True)

# 1. 插入/删除元素：自动保障元素唯一性
r.sadd("product:1001:uids", "1001", "1002", "1003")  # 批量插入用户UID
r.srem("product:1001:uids", "1001")  # 删除指定元素，返回删除成功的数量

# 2. 判断元素是否存在：SISMEMBER命令，返回1存在/0不存在
is_member = r.sismember("product:1001:uids", "1002")

# 3. 随机获取元素：不影响集合中的元素
random_uid = r.srandmember("product:1001:uids", count=1)  # 随机获取1个元素

# 4. 弹出元素：SPOP命令，原子性随机移除并返回一个元素
pop_uid = r.spop("product:1001:uids")

# 5. 集合间的运算：支持多集合的交集/并集/差集
other_set = {"1002", "1003", "1004"}
inter = r.sinter("product:1001:uids", other_set)  # 计算交集
union = r.sunion("product:1001:uids", other_set)  # 计算并集
diff = r.sdiff("product:1001:uids", other_set)  # 计算差集

# 6. 存储集合运算结果：避免大量数据传输，提高后续读取速度
r.sinterstore("product:1001:inter", "product:1001:uids", other_set)  # 存储交集结果