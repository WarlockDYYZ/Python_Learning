from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from redis.asyncio import Redis
from app.models.db import UrlMapping
from app.core.hash import encode_base62


class ShortenerService:
    def __init__(self, db: AsyncSession, redis_client: Redis):
        self.db = db
        self.redis = redis_client

    async def create_short_url(self, original_url: str, expires_at: datetime | None = None) -> UrlMapping:
        # 1. 先查是否已存在相同 URL 的短链（可选去重）
        url_hash = UrlMapping.compute_url_hash(original_url)

        result = await self.db.execute(
            select(UrlMapping).where(UrlMapping.url_hash == url_hash)
        )
        existing = result.scalar_one_or_none()

        if existing and (
                existing.expires_at is None
                or existing.expires_at > datetime.now(timezone.utc)):
            return existing

        # 2. Redis INCR 原子发号
        next_id = await self.redis.incr("short_url:id_generator")

        # 3. Base62 编码生成短码
        short_code = encode_base62(next_id)

        # 4. 写入数据库
        url_mapping = UrlMapping(
            short_code=short_code,
            original_url=original_url,
            url_hash=url_hash,  # 写入哈希值
            expires_at=expires_at,
        )
        self.db.add(url_mapping)
        await self.db.flush()

        # 5. 写入 Redis 缓存
        cache_key = f"short_url:{short_code}"
        ttl = max(1, int((expires_at - datetime.now(timezone.utc)).total_seconds())) if expires_at else None
        if expires_at:
            ttl = max(
                1,
                int((expires_at - datetime.now(timezone.utc)).total_seconds()),
            )
        await self.redis.set(cache_key, original_url, ex=ttl)

        return url_mapping

    async def get_original_url(self, short_code: str) -> str | None:
        # 1. 先查缓存
        cache_key = f"short_url:{short_code}"
        cached_url = await self.redis.get(cache_key)
        if cached_url:
            # 异步更新点击计数（不阻塞响应）
            await self._increment_click_count(short_code)
            return cached_url.decode("utf-8") if isinstance(cached_url, bytes) else cached_url

        # 2. Cache miss，查数据库
        result = await self.db.execute(
            select(UrlMapping).where(UrlMapping.short_code == short_code)
        )
        url_mapping = result.scalar_one_or_none()

        if not url_mapping:
            return None

        # 检查是否过期
        if url_mapping.expires_at and url_mapping.expires_at < datetime.now(timezone.utc):
            return None

        # 3. 回填缓存
        ttl = max(1, int((url_mapping.expires_at - datetime.utcnow()).total_seconds()))
        if url_mapping.expires_at:
            ttl = int((url_mapping.expires_at - datetime.now(timezone.utc)).total_seconds())
        await self.redis.set(cache_key, url_mapping.original_url, ex=ttl)

        # 4. 更新点击计数
        await self._increment_click_count(short_code)

        return url_mapping.original_url

    async def _increment_click_count(self, short_code: str) -> None:
        """异步更新点击计数：先写 Redis，后续定时批量同步 MySQL"""
        counter_key = f"short_url:clicks:{short_code}"
        await self.redis.incr(counter_key)
        # 实际生产中，这里应配合定时任务将 Redis 计数器批量同步到 MySQL











