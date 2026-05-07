class MyMeta(type):
    def __new__(cls, name, bases, attrs):
        # 在创建类时自动添加一个属性
        attrs['created_by'] = "MyMeta"
        return super().__new__(cls, name, bases, attrs)


# 使用元类
class MyClass(metaclass=MyMeta):
    pass


print(MyClass.created_by)  # 输出：MyMeta
