class Animal:
    def __init__(self, species):
        self._species = species  # 保护属性

    @staticmethod
    def _make_sound():  # 保护方法
        print("动物发出声音")


# 子类继承
class Dog(Animal):
    def __init__(self, name):
        super().__init__("狗")
        self._name = name  # 保护属性

    def bark(self):
        print(f"{self._name}汪汪叫")
        self._make_sound()  # 调用父类保护方法
        # 因为声明为静态方法，所以可以通过类名调用
        # Animal._make_sound()


# 创建实例
dog = Dog("旺财")
# 子类中可以访问保护属性和方法
print(dog._species)  # 输出：狗
# IDE 警告：Access to a protected member _species of a class
dog.bark()  # 输出：旺财汪汪叫，然后调用父类的_make_sound()
# 外部直接访问保护成员（不推荐）
print(dog._name)  # 输出：旺财（但会收到IDE警告）
# IDE 警告：Access to a protected member _name of a class
