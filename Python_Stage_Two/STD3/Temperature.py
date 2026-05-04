class Temperature:
    def __init__(self, celsius):
        # 不是直接赋值 self._celsius 而是走 self.celsius
        # = → 自动触发 setter 方法👉 初始化时就自动执行温度合法性校验。
        # 只要是 对象.属性 = 值，就触发 @ 属性名.setter
        self.celsius = celsius  # 使用setter进行初始化

    @property
    def celsius(self):
        # temp.celsius 触发这个方法，返回 _celsius
        # 把方法伪装成属性，读取数据
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        # 赋值拦截 + 数据校验
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度（-273.15°C）")
        self._celsius = value

    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32


# 创建温度对象
temp = Temperature(25)
# 访问属性
print(temp.celsius)  # 输出：25
print(temp.fahrenheit)  # 输出：77.0
# 修改温度
temp.celsius = 30
# 自动进入 celsius 方法：
# 1. 先校验数据合法性
# 2. 合法才赋值给真实变量 self._celsius
# 3. 非法直接抛异常
print(temp.celsius)  # 输出：30
print(temp.fahrenheit)  # 输出：86.0
# 尝试设置无效温度
# temp.celsius = -300  # 报错：ValueError: 温度不能低于绝对零度（-273.15°C）
