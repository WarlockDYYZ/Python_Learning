from fastapi import FastAPI, APIRouter, Path, Query, Body, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from a_response_model import UserCreate
from utils.response import success_response
try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


# 定义标签元数据：用于接口分组，设置显示名称和描述
tags_metadata = [
    {
        "name": "用户管理",
        "description": "处理用户注册、登录、信息查询、更新、删除等操作",
        "externalDocs": {
            "description": "用户模块详细设计文档",
            "url": "https://example.com/docs/user"
        }
    },
    {
        "name": "商品管理",
        "description": "处理商品发布、分页查询、详情获取、库存更新、删除等操作",
        "externalDocs": {
            "description": "商品模块详细设计文档",
            "url": "https://example.com/docs/product"
        }
    },
    {
        "name": "订单管理",
        "description": "处理订单创建、支付状态查询、物流跟踪、取消订单等操作"
    }
]

# 初始化FastAPI应用，配置所有文档相关参数
app = FastAPI(
    title="电商后台系统 API 文档",
    description="""
       ## 系统简介
       这是为后台管理系统提供的RESTful API服务，包含用户、商品、订单三大核心业务模块。
       所有接口统一采用JSON格式交互，全局采用JWT身份认证，接口请求参数和响应格式严格遵循规范。
       ## 技术栈
       - 基于FastAPI+Pydantic开发，实现高性能自动参数校验
       - 采用模块化路由设计，支持业务横向扩展
       - 集成SQLAlchemy异步ORM，适配MySQL/PostgreSQL数据库
       ## 认证说明
       除登录、注册接口外，所有接口需要在请求头中携带Authorization Bearer Token进行身份认证。
   """,
    version="2.1.0",  # API版本号，与生产环境版本对应
    terms_of_service="https://example.com/terms/",  # 服务条款地址
    contact={
        "name": "系统开发团队",
        "url": "https://example.com/contact/",
        "email": "dev@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    # 自定义文档访问路径
    docs_url="/api/internal/docs",  # 自定义Swagger UI访问路径
    redoc_url="/api/internal/redoc",  # 自定义ReDoc访问路径
    openapi_url="/api/internal/openapi.json",  # 自定义OpenAPI JSON地址
    # 传入标签元数据，用于接口分组
    openapi_tags=tags_metadata
)


# 创建模块化路由，指定分组标签
user_router = APIRouter(prefix="/api/users", tags=["用户管理"])
product_router = APIRouter(prefix="/api/products", tags=["商品管理"])
# -------------------------- 用户模块接口示例 --------------------------
@user_router.post(
    "/",
    summary="创建新用户",
    description="""
       注册新用户，需要提交用户名、邮箱、密码等必填字段。
       - 用户名需全局唯一，长度限制2-20个字符
       - 邮箱必须为有效格式，用于后续找回密码、接收系统通知
       - 密码至少8位，建议包含字母、数字和特殊字符
   """,
    response_description="返回创建成功的用户基础信息，不返回敏感字段（如密码）",
    responses={
        201: {"description": "用户创建成功"},
        400: {"description": "请求参数错误或用户名/邮箱已存在"},
        422: {"description": "请求参数校验失败，请检查输入字段格式"}
    }
)
def create_user(
        user: Annotated[UserCreate, Body(..., example={
            "username": "test_user",
            "email": "test@example.com",
            "password": "Test@123456",
            "nickname": "测试用户"
        })]
):
    """
    创建新用户
    - **username**: 用户名（全局唯一，2-20个字符）
    - **email**: 有效邮箱地址
    - **password**: 登录密码（至少8位，包含字母、数字和特殊字符）
    - **nickname**: 用户昵称（可选，最大30个字符）
    """
    return success_response(message="用户创建成功", data={"id": 1, **user.model_dump()})

# -------------------------- 商品模块接口示例 --------------------------
@product_router.get(
    "/{product_id}",
    summary="根据ID查询商品详情",
    description="通过商品ID获取完整的商品信息，包含名称、价格、分类、库存、描述等字段",
    response_description="返回商品完整详情",
    responses={
        200: {"description": "查询成功"},
        404: {"description": "商品不存在"},
        422: {"description": "参数校验失败，商品ID必须为正整数"}
    }
)
def get_product(
        product_id: Annotated[
            int,
            Path(
                ...,
                ge=1,
                description="商品ID，必须为正整数，且不超过100000",
                example=1001
            )
        ]
):
    """
    根据商品ID查询详细信息
    - 路径参数product_id：要查询的商品ID，正整数
    - 响应中包含商品的所有公开字段，不含内部逻辑字段
    """
    if product_id > 100000:
        raise HTTPException(status_code=404, detail="商品不存在")
    return success_response(
        message="查询商品详情成功",
        data={
            "id": product_id,
            "name": "测试商品",
            "price": 99.9,
            "category": "电子设备",
            "stock": 100,
            "description": "这是一个测试商品"
        }
    )

# 挂载路由
app.include_router(user_router)
app.include_router(product_router)