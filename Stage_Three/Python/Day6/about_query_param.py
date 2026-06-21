from fastapi import FastAPI, Query


app = FastAPI()

# 基础查询用法示例
# 查询参数：page（页码，默认1）、page_size（每页条数，默认10）
@app.get("/users", summary="分页查询用户列表")
def get_users(page: int = 1, page_size: int = 10):
    """分页查询系统内用户列表，支持自定义页码和每页显示条数"""
    return {"page": page, "page_size": page_size, "data": [{"id": 1, "username": "test"}]}

# 多条件筛选
try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated
from typing import Optional, List


@app.get("/products", summary="多条件筛选商品")
def filter_products(
        name: Annotated[Optional[str], Query(description="商品名称模糊关键字，不填则查询全部名称")] = None,
        min_price: Annotated[float, Query(ge=0, description="最低价格，不能小于0")] = 0,
        max_price: Annotated[float, Query(ge=0, description="最高价格，必须大于等于最低价格")] = 10000,
        category: Annotated[Optional[str], Query(description="商品分类，不填则查询全部分类")] = None,
        in_stock: Annotated[bool, Query(description="是否仅查询有库存的商品")] = False
):
    """
    根据多条件组合筛选商品
    支持按名称、价格区间、分类、库存状态过滤
    """
    # 模拟业务筛选逻辑：实际项目中会将这些条件拼接为SQL查询条件
    return {
        "filter_conditions": {  # 将接收到的所有筛选条件打包返回，方便前端确认
            "name": name,
            "min_price": min_price,
            "max_price": max_price,
            "category": category,
            "in_stock": in_stock
        },
        "filtered_count": 10,  # 模拟筛选后的总条数
        "data": [{"id": 1001, "name": "测试商品", "price": 99.9}]  # 模拟返回的具体商品列表
    }

# 多值参数
@app.get("/products/tags", summary="按多标签筛选商品")
def get_products_by_tags(
        tags: List[str] = Query(..., description="商品标签列表，支持传入多个标签，匹配任意标签")
):
    """根据多个商品标签筛选商品，满足任意标签条件即可匹配结果"""
    return {"tags": tags, "matching_products": [{"id": 1001, "name": "测试商品"}]}
