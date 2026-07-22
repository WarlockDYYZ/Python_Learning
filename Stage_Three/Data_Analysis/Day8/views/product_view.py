# views/product_view.py
from django.http import JsonResponse
from django.views import View
from django_redis import get_redis_connection
from utils.redis_decorator import log_redis_operation
from models import Product
import json
from django.shortcuts import get_object_or_404


class ProductCacheView(View):
    def get(self, request, product_id):
        # 调用Redis读取商品缓存，自动记录完整的操作日志
        product_data = self.get_product_cache(request, product_id)
        if product_data:
            return JsonResponse({"data": json.loads(product_data), "source": "cache"})

        # 缓存未命中，查询数据库
        product = get_object_or_404(Product, id=product_id)
        product_dict = {
            "id": product.id,
            "name": product.name,
            "price": str(product.price),
            "stock": product.stock
        }

        # 写入Redis缓存，设置1小时过期时间，自动记录日志
        self.set_product_cache(request, product_id, product_dict)
        return JsonResponse({"data": product_dict, "source": "database"})

    # 应用日志装饰器，指定业务场景为product_cache
    @log_redis_operation(biz_type="product_cache")
    def get_product_cache(self, request, product_id):
        """读取商品缓存数据，自动记录操作日志"""
        redis_conn = get_redis_connection("default")
        cache_key = f"product:info:{product_id}"
        return redis_conn.get(cache_key)

    @log_redis_operation(biz_type="product_cache")
    def set_product_cache(self, request, product_id, product_dict):
        """写入商品缓存数据，自动记录操作日志"""
        redis_conn = get_redis_connection("default")
        cache_key = f"product:info:{product_id}"
        # 设置序列化后的缓存数据，过期时间为3600秒（1小时）
        redis_conn.setex(
            cache_key,
            3600,
            json.dumps(product_dict, ensure_ascii=False)
        )