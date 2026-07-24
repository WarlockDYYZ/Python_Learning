# app/api/order.py
from fastapi import APIRouter, HTTPException
import httpx
from app import HttpClientDep
import asyncio


router = APIRouter(prefix="/orders", tags=["订单管理"])

@router.get("/{order_id}/detail", summary="异步获取订单聚合详情")
async def get_order_detail(
    order_id: int,
    client: HttpClientDep  # 注入全局HTTP客户端
):
    """并发调用订单、用户、商品第三方服务，聚合返回详情"""
    try:
        # 并发调用三个无依赖第三方接口
        order_task = client.get(f"/orders/{order_id}")
        user_task = client.get(f"/users/{order_id}")
        goods_task = client.get(f"/goods/{order_id}")

        # 等待所有任务完成，总耗时由最慢的接口决定
        order_res, user_res, goods_res = await asyncio.gather(order_task, user_task, goods_task)

        # 校验第三方接口响应状态
        order_res.raise_for_status()
        user_res.raise_for_status()
        goods_res.raise_for_status()

    except httpx.HTTPStatusError as e:
        # 处理第三方接口返回的错误状态码
        raise HTTPException(status_code=e.response.status_code, detail=f"下游服务异常：{str(e)}")
    except httpx.TimeoutException:
        # 处理请求超时
        raise HTTPException(status_code=504, detail="下游服务请求超时，请稍后重试")
    except httpx.HTTPError as e:
        # 处理其他网络异常
        raise HTTPException(status_code=500, detail=f"下游服务调用失败：{str(e)}")

    # 聚合多方响应结果
    return {
        "order": order_res.json(),
        "user": user_res.json(),
        "goods": goods_res.json()
    }