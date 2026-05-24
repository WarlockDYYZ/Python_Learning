from Some_Projects.Bank_Account_Management_System.account_exceptions import *
from Some_Projects.Bank_Account_Management_System.savings_account import SavingsAccount


class PremiumAccount(SavingsAccount):
    def __init__(self, account_holder, interest_rate=0.03, min_balance=1000):
        super().__init__(account_holder, interest_rate, min_balance)
        self.reward_points = 0

    def deposit(self, amount):
        if amount < 0:
            raise NegativeAmountError(amount)
        # 高级账户存款奖励积分（每$100获得1积分）
        reward = amount // 100
        self.reward_points += reward
        super().deposit(amount)
        self.record_transaction("deposit", amount, f"高级账户存款（奖励{reward}积分）")
        print(f"高级账户{self.account_id}存款${amount}成功，奖励{reward}积分，当前余额：${self._balance}")

    def withdraw(self, amount):
        if amount < 0:
            raise NegativeAmountError(amount)
        # 高级账户免手续费
        super().withdraw(amount)
        self.record_transaction("withdrawal", amount, "高级账户取款（免手续费）")
        print(f"高级账户{self.account_id}取款${amount}成功（免手续费），当前余额：${self._balance}")

    def calculate_rewards(self):
        """计算奖励积分价值（每100积分价值$1）"""
        return self.reward_points / 100

    def redeem_rewards(self, points):
        """兑换积分"""
        if points <= 0 or points > self.reward_points:
            raise ValueError(f"无效的积分兑换：{points}（当前积分：{self.reward_points}）")
        value = points / 100
        self.deposit(value)
        self.reward_points -= points
        print(f"高级账户{self.account_id}兑换{points}积分成功，价值${value:.2f}")
