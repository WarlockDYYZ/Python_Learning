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
