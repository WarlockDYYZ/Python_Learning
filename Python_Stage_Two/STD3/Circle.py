class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        """半径的只读属性"""
        return self._radius

    @property
    def diameter(self):
        """直径的只读属性"""
        return self._radius * 2

    @property
    def area(self):
        """面积的只读属性"""
        return 3.14 * self._radius ** 2


# 创建圆
circle = Circle(5)
# 访问属性（注意：这里使用的是属性访问，而不是方法调用）
print(circle.radius)  # 输出：5
print(circle.diameter)  # 输出：10
print(circle.area)  # 输出：78.5
# 尝试修改只读属性（会失败）
# circle.radius = 10  # 报错：AttributeError: can't set attribute
