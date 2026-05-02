from typing import Protocol


# 1. 定义协议：规定必须有 run() 方法
# Protocol 的作用 = 约定「行为规范」
# 凡是符合我这个 Runnable 协议的类
# 必须有一个叫 run 的方法，而且不需要传参数。
# 这就是制定标准
class Runnable(Protocol):
    def run(self):
        # ... 在 Python 里叫 Ellipsis，省略号。
        # 在这里的意思是：
        # 这里只有方法声明，没有具体实现！
        # 相当于  pass  # 空实现 或 raise NotImplementedError
        ...


# 2. 随便写类，只要有 run()，自动符合协议
class Dog:
    @staticmethod
    def run():
        print("狗跑")


class Cat:
    @staticmethod
    def run():
        print("猫跑")


# 3. 使用协议类型提示
def start_run(obj: Runnable):
    obj.run()


# 全都可以用！
start_run(Dog())
start_run(Cat())
