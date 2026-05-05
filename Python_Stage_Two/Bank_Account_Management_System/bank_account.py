from abc import ABC, abstractmethod
from datetime import datetime


class BankAccount(ABC):
    _next_id = 1000  # 类变量：全局账号计数器

    def __init__(self, account_holder):
        self.account_id = str(BankAccount._next_id)
        BankAccount._next_id += 1
        self.account_holder = account_holder
        self._balance = 0.0
        self._transaction_history = []

    @abstractmethod
    def deposit(self, amount):
        """存款"""
        pass

    @abstractmethod
    def withdraw(self, amount):
        """取款"""
        pass

    def get_balance(self):
        """获取余额"""
        return self._balance

    def get_account_info(self):
        """获取账户信息"""
        return {
            "account_id": self.account_id,
            "account_holder": self.account_holder,
            "balance": self._balance,
            "account_type": self.__class__.__name__
        }

    def _record_transaction(self, transaction_type, amount, description=""):
        """记录交易历史"""
        transaction = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": transaction_type,
            "amount": amount,
            "balance_after": self._balance,
            "description": description
        }
        self._transaction_history.append(transaction)

    def get_transaction_history(self):
        """获取交易历史"""
        return self._transaction_history
