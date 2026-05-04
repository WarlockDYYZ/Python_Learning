class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def area(self):
        """计算矩形面积"""
        return self.width * self.height

    @property
    def perimeter(self):
        """计算矩形周长"""
        return 2 * (self.width + self.height)


# 创建矩形
rect = Rectangle(5, 3)
print(rect.area)  # 输出：15
print(rect.perimeter)  # 输出：16
# 修改属性后计算属性会自动更新
rect.width = 6
rect.height = 4
print(rect.area)  # 输出：24
print(rect.perimeter)  # 输出：20
