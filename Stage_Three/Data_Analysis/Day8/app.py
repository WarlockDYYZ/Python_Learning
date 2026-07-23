# app.py
from flask import Flask
from redis import ConnectionPool
from utils.redis_decorator import log_redis_operation  # 复用Django的装饰器
import json
import redis
from flask import jsonify


app = Flask(__name__)

# 初始化全局Redis连接池
redis_pool = ConnectionPool(
    host="localhost",
    port=6379,
    password="your-redis-password",
    db=0,
    max_connections=20,
    decode_responses=True
)

# 业务路由示例，自动记录Redis操作日志
@app.route("/product/<int:product_id>")
def get_product(product_id):
    # 从全局连接池中获取一个Redis连接
    redis_conn = redis.Redis(connection_pool=redis_pool)
    cache_key = f"product:info:{product_id}"

    # 读取缓存，自动记录日志
    product_data = get_product_cache(redis_conn, cache_key)
    if product_data is None:  # 显式检查空结果
        redis_conn.setex(cache_key, 60, "")  # 空值缓存 60 秒
        return jsonify({"error": "Not Found"}), 404

    # 缓存未命中，查询数据库
    product = {"id": product_id, "name": "无线蓝牙耳机", "price": 299.99, "stock": 100}
    set_product_cache(redis_conn, cache_key, product)
    return {"data": product, "source": "database"}

# 复用日志装饰器
@log_redis_operation(biz_type="product_cache")
def get_product_cache(redis_conn, cache_key):
    try:
        product_data = get_product_cache(redis_conn, cache_key)
    except redis.RedisError:  # 捕获所有 Redis 异常
        product_data = None  # 降级：跳过缓存直接查库
    return product_data

@log_redis_operation(biz_type="product_cache")
def set_product_cache(redis_conn, cache_key, product_dict):
    redis_conn.setex(cache_key, 3600, json.dumps(product_dict, ensure_ascii=False))

if __name__ == "__main__":
    app.run()