from Some_Projects.Bank_Account_Management_System.bank import Bank
from Some_Projects.Bank_Account_Management_System.checking_account import CheckingAccount
from Some_Projects.Bank_Account_Management_System.premium_account import PremiumAccount


def main():
    # 创建银行实例
    bank = Bank()
    # 创建账户
    bank.create_account("savings", "Alice", interest_rate=0.025)
    bank.create_account("checking", "Bob", overdraft_limit=-1000)
    bank.create_account("premium", "Charlie", interest_rate=0.035, min_balance=5000)
    # 存款操作
    bank.get_account("1000").deposit(5000)
    bank.get_account("1001").deposit(3000)
    bank.get_account("1002").deposit(10000)
    # 取款操作
    try:
        bank.get_account("1000").withdraw(2000)
        bank.get_account("1001").withdraw(4000)  # 支票账户可以透支
        bank.get_account("1002").withdraw(3000)
    except Exception as e:
        print(f"操作失败：{e}")
    # 转账操作
    bank.transfer("1000", "1001", 500)
    # 应用利息
    bank.apply_interest_to_all()
    # 高级账户积分兑换
    premium_account = bank.get_account("1002")
    premium_account.redeem_rewards(50)  # 兑换50积分
    # 查询账户信息
    print("n=== 账户详情 ===")
    for account_id in ["1000", "1001", "1002"]:
        account = bank.get_account(account_id)
        info = account.get_account_info()
        print(f"n账户{info['account_id']}详情：")
        print(f"  持有者: {info['account_holder']}")
        print(f"  类型: {info['account_type']}")
        print(f"  余额: ${info['balance']:.2f}")
        if isinstance(account, PremiumAccount):
            print(f"  奖励积分: {account.reward_points}")
            print(f"  积分价值: ${account.calculate_rewards():.2f}")
        if isinstance(account, CheckingAccount):
            print(f"  可用余额: ${account.get_available_balance():.2f}")
            print(f"  透支额度: ${account.overdraft_limit}")
    # 交易历史
    print("n=== 交易历史 ===")
    for transaction in bank.get_account("1000").get_transaction_history():
        print(
            f"{transaction['timestamp']} | {transaction['type']} | ${transaction['amount']:.2f} | 余额: ${transaction['balance_after']:.2f} | {transaction['description']}")


if __name__ == "__main__":
    main()
