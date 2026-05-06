def print_star():
    print(100 * "*")


class Dog:
    pass  # 空类定义


my_dog = Dog()  # 创建Dog类的一个对象
another_dog = Dog()  # 创建另一个Dog类的对象


class Person:
    def __init__(self, name, age):
        self.name = name  # 实例属性：姓名
        self.age = age  # 实例属性：年龄


# 创建对象
alice = Person("Alice", 30)
bob = Person("Bob", 25)
print(alice.name)  # 输出：Alice
print(bob.name)  # 输出：Bob
print_star()


class Person2:
    species = "人类"  # 类属性：物种

    def __init__(self, name, age):
        self.name = name  # 实例属性
        self.age = age  # 实例属性


# 访问类属性
print(Person2.species)  # 输出：人类
# 通过对象访问类属性
alice = Person2("Alice", 30)
print(alice.species)  # 输出：人类
# 修改类属性
Person2.species = "智人"
print(alice.species)  # 输出：智人（所有对象都会看到这个变化）
print_star()


class Person3:
    species = "人类"

    def __init__(self, name):
        self.name = name

    def say_hello(self):  # 实例方法
        print(f"你好，我叫{self.name}，是{self.species}")


# 使用实例方法
alice = Person3("Alice")
alice.say_hello()  # 输出：你好，我叫Alice，是人类
print_star()


class Person4:
    species = "人类"

    @classmethod
    # 第一个参数是cls，代表类本身
    def change_species(cls, new_species):  # 类方法
        cls.species = new_species

    @classmethod
    def get_species(cls):  # 类方法
        return cls.species


# 使用类方法
print(Person4.get_species())  # 输出：人类
Person4.change_species("智人")
print(Person4.get_species())  # 输出：智人
print_star()


class MathUtils:
    @staticmethod
    def add(a, b):  # 静态方法
        return a + b

    @staticmethod
    def multiply(a, b):  # 静态方法
        return a * b


# 使用静态方法
print(MathUtils.add(2, 3))  # 输出：5
print(MathUtils.multiply(4, 5))  # 输出：20
print_star()


class BankAccount:
    def __init__(self, account_holder, balance):
        self.account_holder = account_holder  # 公有属性
        self.balance = balance  # 公有属性

    def deposit(self, amount):  # 公有方法
        if amount > 0:
            self.balance += amount
            print(f"存款成功，当前余额：{self.balance}")

    def withdraw(self, amount):  # 公有方法
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"取款成功，当前余额：{self.balance}")


# 使用公有成员
account = BankAccount("Alice", 1000)
print(account.account_holder)  # 输出：Alice
print(account.balance)  # 输出：1000
account.deposit(500)  # 输出：存款成功，当前余额：1500
print_star()


class BankAccount2:
    def __init__(self, account_holder, balance):
        self.account_holder = account_holder  # 公有属性
        self._balance = balance  # 保护属性（protected，单下划线）

    def deposit(self, amount):  # 公有方法
        if amount > 0:
            self._balance += amount
            print(f"存款成功，当前余额：{self._balance}")

    def withdraw(self, amount):  # 公有方法
        if 0 < amount <= self._balance:
            self._balance -= amount
            print(f"取款成功，当前余额：{self._balance}")


# 使用保护成员
account = BankAccount2("Alice", 1000)
print(account.account_holder)  # 输出：Alice
# ✅ 可以访问，但编辑器会警告（不推荐外部直接访问）
# Access to a protected member _balance of a class
print(account._balance)  # 输出：1000（能运行，但不规范）
account.deposit(500)  # 输出：存款成功，当前余额：1500
print_star()


class BankAccount3:
    def __init__(self, account_holder, balance):
        self.account_holder = account_holder  # 公有属性
        self.__balance = balance  # 私有属性

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"存款成功，当前余额：{self.__balance}")

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            print(f"取款成功，当前余额：{self.__balance}")

    def get_balance(self):  # 公有方法访问私有属性
        return self.__balance


# 使用私有成员
account = BankAccount3("Alice", 1000)
print(account.get_balance())  # 输出：1000
account.deposit(500)  # 输出：存款成功，当前余额：1500
# 尝试直接访问私有属性（会失败）
# print(account.__balance)  # 报错：AttributeError: 'BankAccount3' object has no attribute '__balance'
print_star()


class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print("动物发出声音")


# 定义Dog类，继承自Animal
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)  # 调用父类的构造方法
        self.breed = breed  # 子类特有的属性

    def speak(self):  # 重写父类的speak方法
        print("汪汪！")


# 定义Cat类，继承自Animal
class Cat(Animal):
    def speak(self):  # 重写父类的speak方法
        print("喵喵！")


# 创建对象并测试
dog = Dog("旺财", "中华田园犬")
dog.speak()  # 输出：汪汪！
print(dog.name)  # 输出：旺财
cat = Cat("咪咪")
cat.speak()  # 输出：喵喵！
print_star()









