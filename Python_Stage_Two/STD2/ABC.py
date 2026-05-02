from abc import ABC, abstractmethod


class Payment(ABC):
    @abstractmethod
    # 抽象方法装饰器
    # 作用：子类必须实现这个方法，否则报错！
    # 这是一个抽象类，不能直接实例化
    # 子类必须实现 process_payment()
    # 只定规范，不写具体逻辑
    def process_payment(self, amount):
        pass


class CreditCardPayment(Payment):
    def process_payment(self, amount):
        print(f"信用卡支付 ${amount}")


class PayPalPayment(Payment):
    def process_payment(self, amount):
        print(f"PayPal支付 ${amount}")


# 统一处理
def process_payment(payment: Payment, amount):
    # 参数类型是 父类 Payment
    # 但你可以传 任意子类（信用卡、PayPal……）
    # 会自动调用对应子类的方法
    # → 这就是多态！
    payment.process_payment(amount)


# 多态调用
cc_payment = CreditCardPayment()
pp_payment = PayPalPayment()
process_payment(cc_payment, 100)  # 输出：信用卡支付 $100
process_payment(pp_payment, 200)  # 输出：PayPal支付 $200
