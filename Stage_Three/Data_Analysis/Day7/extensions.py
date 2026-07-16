import redis
from redis.exceptions import RedisError, ConnectionError
import json
from typing import Optional, Dict, Any


class RedisClient:
    """生产级Redis工具类，统一封装连接池、序列化、常用操作"""
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        max_connections: int = 20,
        decode_responses: bool = True
    ):
        # 初始化连接池，复用长连接
        self.pool = redis.ConnectionPool(
            host=host,
            port=port,
            db=db,
            password=password,
            max_connections=max_connections,
            decode_responses=decode_responses,
            socket_timeout=5,  # 读写超时5秒
            socket_connect_timeout=1,  # 连接超时1秒
            socket_keepalive=True  # 开启TCP探活
        )
        # 初始化Redis客户端，绑定连接池
        self.client = redis.Redis(connection_pool=self.pool)

    def get_json(self, key: str) -> Optional[Dict[str, Any]]:
        """
        读取JSON序列化的缓存值，自动反序列化
        :param key: Redis键名
        :return: 反序列化后的字典，不存在或异常返回None
        """
        try:
            data = self.client.get(key)
            return json.loads(data) if data else None
        except (RedisError, json.JSONDecodeError) as e:
            print(f"Redis get_json error: {str(e)}")
            return None

    def set_json(
        self, key: str, value: Dict[str, Any], ex: Optional[int] = None
    ) -> bool:
        """
        将字典对象序列化为JSON，存入Redis
        :param key: Redis键名
        :param value: 待存储的字典对象
        :param ex: 过期时间，单位秒
        """
        try:
            return bool(self.client.set(
            key, json.dumps(value, ensure_ascii=False), ex=ex
        ))
        except RedisError as e:
            print(f"Redis set_json error: {str(e)}")
            return False

    def pipeline(self) -> redis.client.Pipeline:
        """获取管道对象，批量执行命令，减少网络开销"""
        return self.client.pipeline()

    def close(self):
        """关闭连接池，释放所有连接资源"""
        self.pool.disconnect()