class BankAccount:
    def __init__(self, initial_balance):
        self.__balance = initial_balance  # 私有属性

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"存款成功，当前余额：{self.__balance}")

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            print(f"取款成功，当前余额：{self.__balance}")
        else:
            print("余额不足或取款金额无效")

    def get_balance(self):  # 公有方法访问私有属性
        return self.__balance


# 创建账户
account = BankAccount(1000)
# 正常操作
account.deposit(500)  # 输出：存款成功，当前余额：1500
account.withdraw(200)  # 输出：取款成功，当前余额：1300
# 尝试直接访问私有属性（会失败）
# print(account.__balance)  # 报错：AttributeError: 'BankAccount' object has no attribute '__balance'
# 通过名称重整访问（不推荐）
# print(account._BankAccount__balance)  # 输出：1300（不推荐这种做法）
# IDE 警告：Access to a protected member _BankAccount__balance of a class
