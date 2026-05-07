from abc import ABC, abstractmethod
import threading


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
# print(account._balance)  # 输出：1000（能运行，但不规范）
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

    @staticmethod
    def speak():
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


class Shape:
    def area(self):
        pass  # 抽象方法，没有具体实现


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):  # 重写area方法
        return 3.14 * self.radius ** 2


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):  # 重写area方法
        return self.width * self.height


# 多态调用
shapes = [Circle(5), Rectangle(3, 4)]
for shape in shapes:
    print(f"面积：{shape.area()}")
# 输出：
# 面积：78.5
# 面积：12
print_star()


class Duck:
    @staticmethod
    def quack():
        print("嘎嘎！")


class Goose:
    @staticmethod
    def quack():
        print("咕咕！")


class Robot:
    @staticmethod
    def quack():
        print("滴滴！")


# 统一的调用函数
def make_quack(duck_like):
    duck_like.quack()


# 多态调用
duck = Duck()
goose = Goose()
robot = Robot()
make_quack(duck)  # 输出：嘎嘎！
make_quack(goose)  # 输出：咕咕！
make_quack(robot)  # 输出：滴滴！
print_star()


class Payment(ABC):
    @abstractmethod
    def process_payment(self, amount):
        """处理支付"""
        pass

    @abstractmethod
    def refund(self, transaction_id):
        """退款操作"""
        pass


# 具体实现类
class CreditCardPayment(Payment):
    # 实现父类定义的抽象方法
    def process_payment(self, amount):
        print(f"信用卡支付 ${amount}")

    def refund(self, transaction_id):
        print(f"信用卡退款，交易ID：{transaction_id}")


class PayPalPayment(Payment):
    def process_payment(self, amount):
        print(f"PayPal支付 ${amount}")

    def refund(self, transaction_id):
        print(f"PayPal退款，交易ID：{transaction_id}")


# 测试
cc_payment = CreditCardPayment()
paypal_payment = PayPalPayment()
cc_payment.process_payment(100)  # 输出：信用卡支付 $100
paypal_payment.refund("TXN12345")  # 输出：PayPal退款，交易ID：TXN12345
print_star()


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"  # 用户友好的表示

    def __repr__(self):
        return f"Point({self.x}, {self.y})"  # 官方表示

    def __add__(self, other):
        """定义向量加法"""
        return Point(self.x + other.x, self.y + other.y)

    def __len__(self):
        """返回坐标的数量"""
        return 2


# 创建点对象
p1 = Point(2, 3)
p2 = Point(4, 5)
print(str(p1))  # 输出：(2, 3)
print(repr(p1))  # 输出：Point(2, 3)
print(len(p1))  # 输出：2
# 向量加法
p3 = p1 + p2
print(p3)  # 输出：(6, 8)
print_star()


class Circle:
    def __init__(self, radius):
        self._radius = radius  # 使用保护属性

    @property
    def radius(self):
        """获取半径"""
        return self._radius

    @property
    def diameter(self):
        """获取直径（只读属性）"""
        return self._radius * 2

    @property
    def area(self):
        """获取面积（只读属性）"""
        return 3.14 * self._radius ** 2


# 使用
circle = Circle(5)
print(circle.radius)  # 输出：5
print(circle.diameter)  # 输出：10
print(circle.area)  # 输出：78.5
# 访问保护属性
# print(circle._radius)  # 可以输出，警告：Access to a protected member _radius of a class
# 尝试修改只读属性（会失败）
# circle.diameter = 20  # 报错：AttributeError: can't set attribute
print_star()


class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius  # 使用setter进行初始化

    @property
    def celsius(self):
        """获取摄氏温度"""
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        """设置摄氏温度（包含验证逻辑）"""
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度（-273.15°C）")
        self._celsius = value

    @property
    def fahrenheit(self):
        """获取华氏温度（只读）"""
        return self._celsius * 9 / 5 + 32


# 使用
temp = Temperature(25)
print(f"摄氏温度：{temp.celsius}°C")  # 输出：25°C
print(f"华氏温度：{temp.fahrenheit}°F")  # 输出：77°F
temp.celsius = 30
print(f"新的摄氏温度：{temp.celsius}°C")  # 输出：30°C
print(f"新的华氏温度：{temp.fahrenheit}°F")  # 输出：86°F
# 尝试设置无效温度
# temp.celsius = -300  # 报错：ValueError: 温度不能低于绝对零度（-273.15°C）
print_star()


class Config:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.deleter
    def value(self):
        print("正在删除配置值...")
        self._value = None
        print("配置值已删除")


# 使用
config = Config(42)
print(config.value)  # 输出：42
del config.value  # 输出：正在删除配置值... 配置值已删除
print(config.value)  # 输出：None
print_star()


class Engine:
    @staticmethod
    def start():
        print("引擎启动")

    @staticmethod
    def stop():
        print("引擎停止")


class Car:
    def __init__(self):
        self.engine = Engine()  # 组合Engine对象

    def start(self):
        print("汽车启动")
        self.engine.start()  # 委托给引擎对象

    def stop(self):
        print("汽车停止")
        self.engine.stop()  # 委托给引擎对象


# 使用
car = Car()
car.start()  # 输出：汽车启动 引擎启动
car.stop()  # 输出：汽车停止 引擎停止
print_star()


# 简单工厂示例
class Animal:
    def speak(self):
        pass


class Dog(Animal):
    def speak(self):
        return "汪汪！"


class Cat(Animal):
    def speak(self):
        return "喵喵！"


# 工厂函数
def create_animal(animal_type):
    if animal_type == "dog":
        return Dog()
    elif animal_type == "cat":
        return Cat()
    else:
        raise ValueError("未知的动物类型")


# 使用工厂
dog = create_animal("dog")
cat = create_animal("cat")
print(dog.speak())  # 输出：汪汪！
print(cat.speak())  # 输出：喵喵！


# 使用字典改进的工厂模式
# 这个用来工厂类，上面是工厂函数
class AnimalFactory:
    animals = {
        "dog": Dog,  # 键是字符串，值是 【类本身】
        "cat": Cat  # 不是对象！是类！
    }

    @staticmethod
    def create(animal_type):
        if animal_type in AnimalFactory.animals:
            # 先取类 → 再加括号实例化
            return AnimalFactory.animals[animal_type]()
        else:
            raise ValueError(f"未知的动物类型：{animal_type}")


# 使用改进的工厂
dog = AnimalFactory.create("dog")
cat = AnimalFactory.create("cat")
print(dog.speak())  # 输出：汪汪！
print(cat.speak())  # 输出：喵喵！
print_star()


# 基本实现
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


# 测试
s1 = Singleton()
s2 = Singleton()
print(s1 is s2)  # 输出：True（两个变量指向同一个对象）


# 使用装饰器实现的 Pythonic 方式
def singleton(cls):
    # 闭包变量，只会初始化一次，长期保存所有被装饰类的实例
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


# 更严谨的版本，加了锁，防止多线程产生影响
def singleton(cls):
    instances = {}
    lock = threading.Lock()  # 加锁保证线程安全

    def get_instance(*args, **kwargs):
        key = (cls, args, tuple(sorted(kwargs.items())))
        if key not in instances:
            with lock:
                # 双重检查，防止高并发重复创建
                if key not in instances:
                    instances[key] = cls(*args, **kwargs)
        return instances[key]

    return get_instance


@singleton
class DatabaseConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        print(f"连接到数据库：{host}:{port}")


# 使用
db1 = DatabaseConnection("localhost", 3306)
db2 = DatabaseConnection("localhost", 3306)
print(db1 is db2)  # 输出：True
# 第一次调用：创建实例，打印连接信息。
# 第二次调用：直接返回缓存的实例，不会执行 __init__。
# db1 is db2 证明是同一个内存对象。
print_star()


class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        """添加观察者"""
        self._observers.append(observer)

    def detach(self, observer):
        """移除观察者"""
        self._observers.remove(observer)

    def notify(self, message):
        """通知所有观察者"""
        for observer in self._observers:
            observer.update(message)


class Observer:
    def update(self, message):
        """接收通知的方法"""
        pass


class EmailObserver(Observer):
    def update(self, message):
        print(f"发送邮件：{message}")


class SMSObserver(Observer):
    def update(self, message):
        print(f"发送短信：{message}")


# 使用观察者模式
subject = Subject()
# 添加观察者
email_observer = EmailObserver()
sms_observer = SMSObserver()
subject.attach(email_observer)
subject.attach(sms_observer)
# 主题发布消息
subject.notify("服务器故障！")
# 输出：
# 发送邮件：服务器故障！
# 发送短信：服务器故障！
print_star()


# 简单元类示例
class MyMeta(type):
    def __new__(cls, name, bases, attrs):
        # 在创建类时自动添加一个属性
        attrs['created_by'] = "MyMeta"
        return super().__new__(cls, name, bases, attrs)


# 使用元类
class MyClass(metaclass=MyMeta):
    pass


print(MyClass.created_by)  # 输出：MyMeta
