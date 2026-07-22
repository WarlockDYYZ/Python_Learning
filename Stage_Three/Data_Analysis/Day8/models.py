from django.db import models


class Product(models.Model):
    """商品模型"""

    id = models.BigAutoField(primary_key=True, verbose_name="商品ID")

    # 1. 商品名称 (对应视图中的 product.name)
    name = models.CharField(max_length=255, verbose_name="商品名称")

    # 2. 商品价格 (对应视图中的 str(product.price))
    # 注意：视图中使用了 str() 转换，说明 price 可能是 Decimal 或 Float 类型
    # 在电商场景中，强烈建议使用 DecimalField 以避免浮点数精度丢失
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="商品价格")

    # 3. 商品库存 (对应视图中的 product.stock)
    # default=0 保证新建商品时库存默认为0
    stock = models.PositiveIntegerField(default=0, verbose_name="商品库存")

    # 4. 基础审计字段 (推荐添加，方便管理)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "product"
        verbose_name = "商品"
        verbose_name_plural = "商品"

    def __str__(self):
        return self.name