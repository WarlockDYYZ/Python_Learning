from datetime import datetime, timezone
from pydantic import BaseModel, field_validator


class UrlCreate(BaseModel):
    url: str
    expires_at: datetime | None = None

    @field_validator("expires_at", mode="before")
    @classmethod
    def ensure_utc(cls, v):
        if v and isinstance(v, datetime) and v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v

class UrlResponse(BaseModel):
    short_code: str
    original_url: str
    created_at: datetime
    expires_at: datetime | None = None
    click_count: int = 0

class Config:
    from_attributes = True