from abc import ABC, abstractmethod


class DiscountStrategy:
    @abstractmethod
    def apply_discount(self, price):
        pass


class NormalDiscount(DiscountStrategy):
    def apply_discount(self, price):
        return price * 0.95  # 5%折扣


class VIPDiscount(DiscountStrategy):
    def apply_discount(self, price):
        return price * 0.85  # 15%折扣


class DiamondDiscount(DiscountStrategy):
    def apply_discount(self, price):
        return price * 0.75  # 25%折扣


# 动态切换策略
class ShoppingCart:
    def __init__(self, discount_strategy: DiscountStrategy):
        self.discount_strategy = discount_strategy

    def calculate_total(self, original_price):
        return self.discount_strategy.apply_discount(original_price)


# 不同用户使用不同策略
normal_cart = ShoppingCart(NormalDiscount())
vip_cart = ShoppingCart(VIPDiscount())
diamond_cart = ShoppingCart(DiamondDiscount())
print(normal_cart.calculate_total(100))  # 输出：95.0
print(vip_cart.calculate_total(100))  # 输出：85.0
print(diamond_cart.calculate_total(100))  # 输出：75.0
