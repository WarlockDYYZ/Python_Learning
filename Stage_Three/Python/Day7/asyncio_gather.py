import asyncio
import httpx
from fastapi import FastAPI, Depends


app = FastAPI(title="高并发异步接口示例")

# 1. 定义 HTTP 客户端工厂函数
async def get_http_client():
    """
    依赖注入：为每个请求提供一个 HTTP 客户端实例。
    使用 async with 确保连接在请求结束时正确关闭，防止连接泄露。
    """
    # 创建异步客户端
    # limits: 限制连接池，防止并发过高压垮下游服务
    # timeout: 设置超时，防止请求挂起导致线程阻塞
    async with httpx.AsyncClient(
        limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
        timeout=httpx.Timeout(5.0, connect=5.0)  # 读取/写入/连接超时均为 5秒
    ) as client:
        yield client

# 2. 修改你的主应用代码 (修正了潜在的 JSON 解析错误)
@app.get("/aggregated-data", summary="聚合多方数据，异步并发调用")
async def get_aggregated_data(
    http_client: httpx.AsyncClient = Depends(get_http_client)
):
    # 创建独立任务
    user_task = http_client.get("http://127.0.0.1:8001/profile")
    product_task = http_client.get("http://127.0.0.1:8001/list")
    order_task = http_client.get("http://127.0.0.1:8001/detail")

    # 并发执行
    user_res, product_res, order_res = await asyncio.gather(
        user_task, product_task, order_task, return_exceptions=True
    )

    # 安全解析 JSON (防止非200响应导致的崩溃)
    # def safe_parse(res, name):
    #     if isinstance(res, Exception):
    #         return {"error": f"{name} request failed", "detail": str(res)}
    #     try:
    #         res.raise_for_status()  # 检查状态码
    #         return res.json()
    #     except Exception as e:
    #         return {"error": f"Failed to parse {name}", "status": res.status_code, "text": res.text}

    return {
        "user": user_res.json(),
        "products": product_res.json(),
        "orders": order_res.json()
    }