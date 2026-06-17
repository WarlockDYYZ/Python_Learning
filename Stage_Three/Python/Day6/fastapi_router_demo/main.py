from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# 导入模块化路由实例
from routers.user import user_router
from routers.product import product_router


# 初始化FastAPI应用，配置全局文档元信息
app = FastAPI(
    title="电商后台管理系统 API",
    description="""
   这是一个标准的模块化FastAPI后台管理系统API文档，包含以下核心业务模块：
   - 👤 用户管理模块：提供用户注册、查询、更新、删除等基础操作
   - 📦 商品管理模块：提供商品发布、分页查询、详情获取、更新、删除等操作
   ## 技术栈说明
   - 基于FastAPI+Pydantic开发，自动实现参数校验和接口文档生成
   - 采用模块化路由设计，支持业务横向扩展
   - 全局统一响应格式，适配前后端对接规范
   """,
    version="1.0.0",
    docs_url="/api-docs",  # 自定义Swagger UI访问路径
    redoc_url="/api-redoc",  # 自定义ReDoc访问路径
    openapi_tags=[
        {"name": "用户管理", "description": "处理用户注册、查询、更新、删除等操作"},
        {"name": "商品管理", "description": "处理商品发布、查询、更新、删除等操作"},
    ]
)
# 配置跨域中间件（CORS），解决前端跨域调试问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境允许所有源，生产环境需指定具体域名
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP请求方法
    allow_headers=["*"],  # 允许所有请求头
)
# 挂载模块化路由
app.include_router(user_router)
app.include_router(product_router)
# 根路径测试接口
@app.get("/", summary="系统根路径测试")
def root():
    return {"message": "欢迎使用电商后台管理系统 API"}