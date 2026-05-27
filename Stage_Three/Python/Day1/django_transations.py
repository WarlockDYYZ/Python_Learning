from django.db import transaction


# 原子请求配置（settings.py）
ATOMIC_REQUESTS = True

# 显式事务示例
@transaction.atomic
def transfer_money(from_account_id, to_account_id, amount):
    # 使用 select_for_update() 获取行级锁，防止并发修改
    from_account = Account.objects.select_for_update().get(id=from_account_id)
    to_account = Account.objects.select_for_update().get(id=to_account_id)

    if from_account.balance < amount:
        raise ValueError("余额不足")

    # 扣款操作
    from_account.balance -= amount
    from_account.save()

    # 加款操作
    to_account.balance += amount
    to_account.save()