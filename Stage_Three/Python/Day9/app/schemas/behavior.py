from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel, Field


class BehaviorCreate(BaseModel):
    """记录行为请求"""
    user_id: int = Field(..., description="用户 ID")
    action_type: str = Field(..., min_length=1, max_length=30, description="行为类型")
    target_id: Optional[str] = Field(None, max_length=100, description="目标 ID")
    metadata: Optional[dict[str, Any]] = Field(None, description="附加数据")


class BehaviorResponse(BaseModel):
    """行为记录响应"""
    id: int
    user_id: int
    action_type: str
    target_id: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class BehaviorListResponse(BaseModel):
    """行为列表响应"""
    total: int
    items: list[BehaviorResponse]
    page: int
    page_size: int


class BehaviorStatsResponse(BaseModel):
    """行为统计响应"""
    user_id: int
    total_count: int
    action_breakdown: dict[str, int]  # 各行为类型的数量