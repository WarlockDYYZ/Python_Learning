from Some_Projects.Bank_Account_Management_System.bank_account import BankAccount
from Some_Projects.Bank_Account_Management_System.account_exceptions import *


class CheckingAccount(BankAccount):
    # 支票账户默认有500的透支额度，每次交易有2.5的交易费
    def __init__(self, account_holder, overdraft_limit=-500, transaction_fee=2.5):
        super().__init__(account_holder)
        self.overdraft_limit = overdraft_limit
        self.transaction_fee = transaction_fee

    def deposit(self, amount):
        if amount < 0:
            raise NegativeAmountError(amount)
        self._balance += amount
        self.record_transaction("deposit", amount, "支票账户存款")
        print(f"支票账户{self.account_id}存款${amount}成功，当前余额：${self._balance}")

    def withdraw(self, amount):
        if amount < 0:
            raise NegativeAmountError(amount)
        # 计算扣除手续费后的实际取款金额
        actual_amount = amount + self.transaction_fee
        if self._balance - actual_amount < self.overdraft_limit:
            raise InsufficientFundsError(self.account_id, self._balance, actual_amount)
        self._balance -= actual_amount
        self.record_transaction("withdrawal", amount, f"支票账户取款（手续费${self.transaction_fee}）")
        print(f"支票账户{self.account_id}取款${amount}成功（手续费${self.transaction_fee}），当前余额：${self._balance}")

    def get_available_balance(self):
        """获取可用余额（包括透支额度）"""
        return self._balance + self.overdraft_limit
