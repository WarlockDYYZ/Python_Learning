from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from app.models.schemas import UrlCreate, UrlResponse
from app.services.shortener import ShortenerService
from app.api.deps import get_db, get_redis


router = APIRouter(tags=["shortener"])

@router.post("/shorten", response_model=UrlResponse,
status_code=status.HTTP_201_CREATED)
async def create_short_url(
    payload: UrlCreate,
    db: AsyncSession = Depends(get_db),
    redis_client: Redis = Depends(get_redis),
):
    service = ShortenerService(db, redis_client)
    url_mapping = await service.create_short_url(
        original_url=payload.url,
        expires_at=payload.expires_at
    )
    return url_mapping

@router.get("/{short_code}")
async def redirect_short_url(
    short_code: str,
    db: AsyncSession = Depends(get_db),
    redis_client: Redis = Depends(get_redis),
):
    service = ShortenerService(db, redis_client)
    original_url = await service.get_original_url(short_code)
    if not original_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found or expired",
        )
    # 使用 302 临时重定向，确保每次请求都经过服务以统计点击量
    return RedirectResponse(url=original_url, status_code=status.HTTP_302_FOUND)