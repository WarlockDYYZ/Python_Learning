class Animal:
    def speak(self):
        print("动物发出声音")


class Dog(Animal):
    def speak(self):  # 重写父类方法
        print("汪汪叫")


class Cat(Animal):
    def speak(self):  # 重写父类方法
        print("喵喵叫")


# 多态调用
def animal_speak(animal: Animal):
    animal.speak()


dog = Dog()
cat = Cat()
animal_speak(dog)  # 输出：汪汪叫
animal_speak(cat)  # 输出：喵喵叫
