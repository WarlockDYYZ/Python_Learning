class AnimalFactory:
    animals = {
        "dog": Dog,
        "cat": Cat
    }

    @staticmethod
    def create(animal_type):
        if animal_type in AnimalFactory.animals:
            return AnimalFactory.animals[animal_type]()
        else:
            raise ValueError(f"未知的动物类型：{animal_type}")


# 使用改进的工厂
dog = AnimalFactory.create("dog")
cat = AnimalFactory.create("cat")
