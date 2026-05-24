from Some_Projects.Bank_Account_Management_System.account_exceptions import *
from Some_Projects.Bank_Account_Management_System.checking_account import CheckingAccount
from Some_Projects.Bank_Account_Management_System.premium_account import PremiumAccount
from Some_Projects.Bank_Account_Management_System.savings_account import SavingsAccount


class Bank:
    def __init__(self):
        self.accounts = {}  # 存储所有账户

    def create_account(self, account_type, account_holder, **kwargs):
        """创建账户"""
        account_types = {
            "savings": SavingsAccount,
            "checking": CheckingAccount,
            "premium": PremiumAccount
        }
        if account_type not in account_types:
            raise ValueError(f"不支持的账户类型：{account_type}")
        account_class = account_types[account_type]
        account = account_class(account_holder, **kwargs)
        self.accounts[account.account_id] = account
        print(f"创建{account_type}账户{account.account_id}成功，持有者：{account_holder}")
        return account

    def get_account(self, account_id):
        """获取账户"""
        if account_id not in self.accounts:
            raise AccountNotFoundError(account_id)
        return self.accounts[account_id]

    def list_accounts(self):
        """列出所有账户"""
        print("n=== 所有账户列表 ===")
        for account in self.accounts.values():
            info = account.get_account_info()
            print(
                f"ID: {info['account_id']} | 类型: {info['account_type']} | 持有者: {info['account_holder']}"
                f" | 余额: ${info['balance']:.2f}")

    def transfer(self, from_account_id, to_account_id, amount):
        """转账"""
        if amount < 0:
            raise NegativeAmountError(amount)
        from_account = self.get_account(from_account_id)
        to_account = self.get_account(to_account_id)
        try:
            from_account.withdraw(amount)
            to_account.deposit(amount)
            print(f"转账成功：从{from_account_id}转${amount}到{to_account_id}")
            # 记录转账交易
            from_account.record_transaction("transfer", amount, f"转账到{to_account_id}")
            to_account.record_transaction("transfer", amount, f"来自{from_account_id}的转账")
        except InsufficientFundsError as e:
            print(f"转账失败：{e}")
        except Exception as e:
            print(f"转账失败：{e}")

    def apply_interest_to_all(self):
        """对所有储蓄账户应用利息"""
        print("\n=== 应用利息 ===")
        for account in self.accounts.values():
            # 打印储蓄账户和高级账户的利息
            if isinstance(account, SavingsAccount):
                account.apply_interest()
