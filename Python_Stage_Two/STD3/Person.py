class Person:
    def __init__(self, name, age):
        self.name = name  # 公有属性
        self.age = age  # 公有属性

    def say_hello(self):  # 公有方法
        print(f"你好，我叫{self.name}，今年{self.age}岁")


# 创建实例
p = Person("Alice", 30)
# 直接访问公有属性
print(p.name)  # 输出：Alice
print(p.age)  # 输出：30
# 调用公有方法
p.say_hello()  # 输出：你好，我叫Alice，今年30岁
