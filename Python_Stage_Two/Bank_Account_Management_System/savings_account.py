from Python_Stage_Two.Bank_Account_Management_System.bank_account import BankAccount
from Python_Stage_Two.Bank_Account_Management_System.account_exceptions import *


class SavingsAccount(BankAccount):
    def __init__(self, account_holder, interest_rate=0.02, min_balance=100):
        super().__init__(account_holder)
        self.interest_rate = interest_rate
        self.min_balance = min_balance

    def deposit(self, amount):
        if amount < 0:
            raise NegativeAmountError(amount)
        self._balance += amount
        self.record_transaction("deposit", amount, "储蓄账户存款")
        print(f"储蓄账户{self.account_id}存款${amount}成功，当前余额：${self._balance}")

    def withdraw(self, amount):
        if amount < 0:
            raise NegativeAmountError(amount)
        if self._balance - amount < self.min_balance:
            raise InsufficientFundsError(self.account_id, self._balance, amount)
        self._balance -= amount
        self.record_transaction("withdrawal", amount, "储蓄账户取款")
        print(f"储蓄账户{self.account_id}取款${amount}成功，当前余额：${self._balance}")

    def calculate_interest(self):
        """计算利息"""
        interest = self._balance * self.interest_rate
        return interest

    def apply_interest(self):
        """应用利息"""
        interest = self.calculate_interest()
        self.deposit(interest)
        self.record_transaction("interest", interest, f"年利率{self.interest_rate * 100}%")
        print(f"储蓄账户{self.account_id}已应用利息${interest:.2f}")
