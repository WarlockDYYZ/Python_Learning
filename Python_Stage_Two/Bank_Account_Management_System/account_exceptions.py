class InsufficientFundsError(Exception):
    """余额不足异常"""
    def __init__(self, account_id, balance, amount):
        self.account_id = account_id
        self.balance = balance
        self.amount = amount
        super().__init__(f"账户{account_id}余额不足（${balance} < ${amount}）")


class NegativeAmountError(Exception):
    """金额为负异常"""
    def __init__(self, amount):
        self.amount = amount
        super().__init__(f"金额不能为负数：${amount}")


class AccountNotFoundError(Exception):
    """账户未找到异常"""
    def __init__(self, account_id):
        self.account_id = account_id
        super().__init__(f"账户{account_id}不存在")
