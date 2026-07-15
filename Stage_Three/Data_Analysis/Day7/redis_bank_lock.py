import redis

r = redis.Redis(decode_responses=True)

def transfer(from_acc: str, to_acc: str, amount: int):
    # 循环重试，直到转账成功
    while True:
        # 1. 监听转出账户的余额键
        r.watch(from_acc)
        # 2. 读取转出账户的当前余额
        # 显示转换类型消除编辑器警告
        # balance = int(r.get(from_acc) or 0)
        balance = int(str(r.get(from_acc) or 0))
        if balance < amount:
            r.unwatch()
            raise ValueError("余额不足，无法完成转账")
        # 3. 开启事务，打包执行扣减、新增命令
        pipe = r.pipeline(transaction=True)
        pipe.decrby(from_acc, amount)
        pipe.incrby(to_acc, amount)
        try:
            # 4. 执行事务，如果键被修改则抛出WatchError
            pipe.execute()
            r.unwatch()
            break
        except redis.WatchError:
            # 发生并发冲突，重试
            continue