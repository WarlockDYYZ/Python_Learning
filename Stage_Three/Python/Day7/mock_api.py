from fastapi import FastAPI
import uvicorn


app = FastAPI()

# 模拟用户服务
@app.get("/profile")
async def user_profile():
    return {"user_id": 9527, "name": "测试用户", "level": "VIP"}

# 模拟商品服务
@app.get("/list")
async def product_list():
    return {"products": [{"id": 101, "name": "测试商品A"}, {"id": 102, "name": "测试商品B"}]}

# 模拟订单服务
@app.get("/detail")
async def order_detail():
    return {"order_id": "ORD-2026", "status": "success", "amount": 99.9}

if __name__ == "__main__":
    # 在本地 8001 端口启动服务
    uvicorn.run(app, host="127.0.0.1", port=8001)