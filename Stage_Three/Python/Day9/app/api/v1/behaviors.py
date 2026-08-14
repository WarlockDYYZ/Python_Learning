# app/api/v1/behaviors.py
from fastapi import APIRouter, Depends
from app.models.user import User
from app.api.deps import check_user_permission

router = APIRouter()

# 仅管理员可以调用批量导出行为数据的接口
@router.get("/export", summary="导出所有用户行为数据")
def export_behaviors(current_user: User = Depends(check_user_permission(["admin"]))):
    return {"data": "所有行为数据的导出文件地址"}

# 普通用户和管理员都可以调用查看自身行为数据的接口
@router.get("/mine", summary="查看我的行为数据")
def get_my_behaviors(current_user: User = Depends(check_user_permission(["admin", "user"]))):
    return {"data": "当前用户的行为数据列表"}