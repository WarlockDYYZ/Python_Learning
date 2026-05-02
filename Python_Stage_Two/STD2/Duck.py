class Duck:
    @staticmethod
    def quack():
        print("嘎嘎叫")


class Goose:
    @staticmethod
    def quack():
        print("咕咕叫")


class Robot:
    @staticmethod
    def quack():
        print("滴滴声")


# 统一接口
# 这里不限制传入参数的类型，不同与Animal
def make_quack(duck_like):
    duck_like.quack()


# 多态调用
duck = Duck()
goose = Goose()
robot = Robot()
make_quack(duck)  # 输出：嘎嘎叫
make_quack(goose)  # 输出：咕咕叫
make_quack(robot)  # 输出：滴滴声
