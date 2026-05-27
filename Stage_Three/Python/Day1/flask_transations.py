from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError


# 转账事务示例
def transfer_money(from_account_id, to_account_id, amount):
    try:
        # 开启事务
        db.session.begin_nested()

        # 扣款操作
        from_account = Account.query.get(from_account_id)
        from_account.balance -= amount

        # 加款操作
        to_account = Account.query.get(to_account_id)
        to_account.balance += amount

        # 提交事务
        db.session.commit()
        return True
    except IntegrityError as e:
        # 回滚事务
        db.session.rollback()
        print(f"事务失败: {e}")
        return False
    finally:
        db.session.close()