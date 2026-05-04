class Config:
    def __init__(self, value):
        # 真实数据存在：私有变量 self._value
        # value 只是包装出来的属性，不是真实存储字段
        self._value = value

    @property
    def value(self):
        # config.value 对外暴露 value 属性，只读（没有 setter），本质就是返回内部 _value
        return self._value

    @value.deleter
    def value(self):
        # del config.value 自动运行这个 eleter 方法
        # 1. 打印日志提示
        # 2. 把底层真实数据 self._value 重置为 None
        # 3. 再打印结束提示
        print("正在删除配置值...")
        self._value = None
        print("配置值已删除")


# 创建配置对象
config = Config(42)
# 访问属性
print(config.value)  # 输出：42
# 删除属性
del config.value  # 输出：正在删除配置值... 配置值已删除
# 再次访问（已被删除）
print(config.value)  # 输出：None
