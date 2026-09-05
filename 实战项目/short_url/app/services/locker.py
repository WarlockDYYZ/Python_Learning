import asyncio
import json
import random
from app.services.cache import local_cache
from app.core.redis import redis_client


class ShortLinkService:
    BASE_TTL = 300  # 基础 TTL（秒）

    async def get_original_url_with_lock(self, short_code: str) -> str | None:
        """带分布式锁的缓存查询，解决缓存击穿"""
        # 1. 先查本地缓存
        local_val = local_cache.get(short_code)
        if local_val is not None:
            return local_val

        # 2. 查 Redis
        redis_key = f"short_link:{short_code}"
        redis_val = await redis_client.get(redis_key)
        if redis_val is not None:
            url = json.loads(redis_val)
            local_cache.set(short_code, url)
            return url

        # 3. 缓存 miss，尝试获取分布式锁
        lock_key = f"lock:short_link:{short_code}"
        # SETNX + ex=10 防止持锁进程崩溃导致死锁
        acquired = await redis_client.set(lock_key, "1", nx=True, ex=10)

        if acquired:
            try:
                # 4. 双重检查（Double-Check）：拿到锁后再查一次缓存
                redis_val = await redis_client.get(redis_key)
                if redis_val is not None:
                    url = json.loads(redis_val)
                    local_cache.set(short_code, url)
                    return url

                # 5. 真正查库
                url = await self._fetch_from_db(short_code)
                if url:
                    # TTL 随机化，防止缓存雪崩
                    ttl = self.BASE_TTL + random.randint(-30, 30)
                    await redis_client.set(redis_key, json.dumps(url), ex=ttl)
                    local_cache.set(short_code, url)
                return url
            finally:
                # 6. 释放锁
                await redis_client.delete(lock_key)
        else:
            # 7. 没拿到锁，等待重试
            await asyncio.sleep(0.1)
            return await self.get_original_url_with_lock(short_code)

    async def _fetch_from_db(self, short_code: str) -> str | None:
        """从数据库查询原始 URL（示意）"""
        # 实际实现：查询 MySQL
        return None