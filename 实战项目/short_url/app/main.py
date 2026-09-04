from fastapi import FastAPI
from app.config import settings
from app.api.routes import shortener, stats


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)

# 注册路由
app.include_router(shortener.router)
app.include_router(stats.router, prefix="/api/stats")
@app.get("/health")
async def health_check():
    return {"status": "ok", "service": settings.APP_NAME}