import pymysql


# 建立数据库连接
conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='your_password',
    database='transaction_db',
    charset='utf8mb4'
)
# 创建游标
cursor = conn.cursor()

def transfer_money(from_account_id, to_account_id, amount):
    """银行转账事务"""
    try:
        conn.autocommit(False)
        # 1. 查询转出账户余额
        cursor.execute("SELECT balance FROM accounts WHERE id = %s", (from_account_id,))
        from_balance = cursor.fetchone()[0]
        # 2. 检查余额是否充足
        if from_balance < amount:
            raise ValueError("余额不足，转账失败")
        # 3. 执行转账
        cursor.execute("UPDATE accounts SET balance = balance - %s WHERE id = %s", (amount, from_account_id))
        cursor.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, to_account_id))
        # 4. 记录转账日志
        cursor.execute("""
           INSERT INTO transfer_logs (from_account_id, to_account_id, amount, create_time)
           VALUES (%s, %s, %s, NOW())
       """, (from_account_id, to_account_id, amount))
        conn.commit()
        return True, "转账成功"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.autocommit(True)

# 使用示例
success, message = transfer_money(1, 2, 100)
print(f"转账结果: {'成功' if success else '失败'}, 消息: {message}")