from datetime import timezone
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator
from urllib.parse import urlparse
import ipaddress


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

class UrlCreate(BaseModel):
    url: str = Field(..., description="原始长链接")
    custom_code: str | None = Field(None, description="自定义短码")
    expires_at: datetime | None = Field(None, description="过期时间")

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """URL 格式校验 + SSRF 防护"""
        parsed = urlparse(v)
        if parsed.scheme not in ("http", "https"):
            raise ValueError("仅支持 http/https 协议")
        if not parsed.hostname:
            raise ValueError("URL 缺少主机名")

        # SSRF 防护：拦截内网地址
        try:
            ip = ipaddress.ip_address(parsed.hostname)
            if ip.is_private or ip.is_loopback or ip.is_link_local:
                raise ValueError("不允许访问内网地址")
        except ValueError:
            # 非 IP 格式（域名），此处简化处理
            # 生产环境应做 DNS 解析后再判断
            pass

        return v

    @field_validator("custom_code")
    @classmethod
    def validate_custom_code(cls, v: str | None) -> str | None:
        """自定义短码校验：仅允许字母数字，长度 3-20"""
        if v is None:
            return v
        if not v.isalnum():
            raise ValueError("自定义短码只能包含字母和数字")
        if len(v) < 3 or len(v) > 20:
            raise ValueError("自定义短码长度需在 3-20 之间")
        return v

    @model_validator(mode="after")
    def validate_expires_at(self):
        """过期时间必须晚于当前时间"""
        if self.expires_at and self.expires_at <= datetime.now(timezone.utc):
            raise ValueError("过期时间必须晚于当前时间")
        return self