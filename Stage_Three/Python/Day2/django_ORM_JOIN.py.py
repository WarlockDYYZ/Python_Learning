# 第一步：先配置 Django 环境，必须放在最前面！
import os
import django
from django.conf import settings

# 手动配置 Django（不用创建项目！）
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="test-key-12345",
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
        ],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": "mydatabase2.db",
            }
        }
    )
    django.setup()


# 模型定义
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "django.contrib.auth"  # 用系统自带的，不用新建APP


class Order(models.Model):
    # 加 related_name='orders'
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'  # 必须加！
    )
    order_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=(
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ))

    class Meta:
        app_label = "django.contrib.auth"  # 用系统自带的，不用新建APP


# 测试：创建表
from django.db import connection
with connection.schema_editor() as editor:
    editor.create_model(User)
    editor.create_model(Order)

print("Django ORM 模型运行成功！")


# 插入数据
from datetime import datetime

# 清空旧数据
Order.objects.all().delete()
User.objects.all().delete()

# 创建 5 个用户
user1 = User.objects.create(username="张三", email="zhangsan@test.com")
user2 = User.objects.create(username="李四", email="lisi@test.com")
user3 = User.objects.create(username="王五", email="wangwu@test.com")
user4 = User.objects.create(username="赵六", email="zhaoliu@test.com")
user5 = User.objects.create(username="钱七", email="qianqi@test.com")

Order.objects.create(user=user1, order_date=datetime(2023,1,10), amount=100.50, status="completed")
Order.objects.create(user=user1, order_date=datetime(2023,2,15), amount=200.00, status="completed")
Order.objects.create(user=user1, order_date=datetime(2023,3,20), amount=150.00, status="completed")

Order.objects.create(user=user2, order_date=datetime(2023,1,12), amount=150.75, status="completed")
Order.objects.create(user=user2, order_date=datetime(2023,3,20), amount=300.25, status="completed")
Order.objects.create(user=user2, order_date=datetime(2023,4,15), amount=220.00, status="completed")

Order.objects.create(user=user3, order_date=datetime(2023,2,20), amount=50.00, status="completed")
Order.objects.create(user=user3, order_date=datetime(2023,4,10), amount=75.50, status="completed")

Order.objects.create(user=user4, order_date=datetime(2023,3,1), amount=400.00, status="completed")
Order.objects.create(user=user4, order_date=datetime(2023,5,1), amount=350.00, status="completed")

Order.objects.create(user=user5, order_date=datetime(2023,1,5), amount=80.50, status="completed")
Order.objects.create(user=user5, order_date=datetime(2023,2,8), amount=90.25, status="completed")
Order.objects.create(user=user5, order_date=datetime(2023,3,9), amount=100.00, status="completed")
Order.objects.create(user=user5, order_date=datetime(2023,4,12), amount=120.75, status="completed")
Order.objects.create(user=user5, order_date=datetime(2023,5,15), amount=130.20, status="completed")
Order.objects.create(user=user5, order_date=datetime(2023,6,1), amount=140.80, status="completed")

print("5 个用户，16 条订单插入成功！")


# 统计每个用户的订单总数和总金额
from django.db.models import Count, Sum, Max, F

# 1. 统计每个用户的订单总数和总金额（从订单表查询）
user_orders = Order.objects.values(
    username=F("user__username")
).annotate(
    order_count=Count("id"),
    total_spent=Sum("amount")
).filter(order_count__gte=2).order_by("-total_spent")

print("Django ORM分组查询结果：")
for item in user_orders:
    print(f"用户: {item['username']}, 订单数: {item['order_count']}, 总消费: {item['total_spent']}")

# 2. 查询每个用户最近订单日期（安全、兼容所有版本）
last_orders = Order.objects.values(
    username=F("user__username")
).annotate(
    last_order_date=Max("order_date")
).order_by("user_id")

print("\n带自定义查询的结果：")
for item in last_orders:
    print(f"用户: {item['username']}, 最近订单日期: {item['last_order_date']}")