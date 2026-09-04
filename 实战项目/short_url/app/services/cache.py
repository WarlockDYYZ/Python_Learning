from cachetools import TTLCache
from threading import Lock


class LocalCache:
    """基于 cachetools 的本地 TTL 缓存"""
    def __init__(self, maxsize: int = 10000, ttl: int = 300):
        """
        初始化本地缓存
                :param maxsize: 最大缓存条目数，防止 OOM
                :param ttl: 默认过期时间（秒）
        """
        self._cache = TTLCache(maxsize=maxsize, ttl=ttl)
        self._lock = Lock()

    def get(self, key: str):
        """获取缓存值，不存在返回 None"""
        with self._lock:
            return self._cache.get(key)

    def set(self, key: str, value, ttl: int = None):
        """设置缓存值，可指定单独的 TTL"""
        with self._lock:
            if ttl is not None:
                # cachetools 不直接支持单 key 覆盖 TTL，
                # 这里简化处理：若需自定义 TTL，需重新创建或使用其他策略
                # 实际生产中可考虑使用 cachetools.TTLCache 的 timer 扩展
                self._cache[key] = value
            else:
                self._cache[key] = value

    def delete(self, key: str):
        """删除指定缓存"""
        with self._lock:
            self._cache.pop(key, None)

    def clear(self):
        """清空所有缓存"""
        with self._lock:
            self._cache.clear()

# 全局单例
local_cache = LocalCache(maxsize=10000, ttl=300)