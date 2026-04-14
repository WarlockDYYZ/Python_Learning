name = input("name")
age = int(input('age'))
height = float(input('height'))
print(f'\n个人信息')
print(f'{name}')
print(f'{age}')
print(f'{height}')
print(f'明年年龄{age+1}')

# 题目：指出下列变量的数据类型
# int
var1 = 42
# float
var2 = 3.14
# str
var3 = "Hello, World!"
# bool
var4 = True
# list
var5 = [1, 2, 3]
# dict
var6 = {"name": "Alice", "age": 30}
# 验证
print("变量类型判断：")
print(f"var1: {type(var1)}")
print(f"var2: {type(var2)}")
print(f"var3: {type(var3)}")
print(f"var4: {type(var4)}")
print(f"var5: {type(var5)}")
print(f"var6: {type(var6)}")

# 变量交换
a = 5
b = 10
print(f'原来:a={a} b={b}')
a, b = b, a
print(f'交换:a={a} b={b}')

# 完成以下数据类型转换
num_str = "123"
float_num = 3.9
bool_val = True
# 1. 将num_str转换为整数
int_num = int(num_str)
# 2. 将float_num转换为整数
int_float = int(float_num)
# 3. 将bool_val转换为整数
int_bool = int(num_str)
# 4. 将整数100转换为字符串
str_num = str('100')
print(f"类型转换结果：")
print(f"int_num: {int_num}, 类型: {type(int_num)}")
print(f"int_float: {int_float}, 类型: {type(int_float)}")
print(f"int_bool: {int_bool}, 类型: {type(int_bool)}")
print(f"str_num: {str_num}, 类型: {type(str_num)}")

# 字符串操作
s = 'Hello, Python'
print(len(s))
print(s[0])
print(s[-1])
print(s[7:])
print(s.upper())
print(s.replace('Python', 'World'))

# 算术运算符
a = 10
b = 3
print(f"加法: {a} + {b} = {a + b}")
print(f"减法: {a} - {b} = {a - b}")
print(f"乘法: {a} * {b} = {a * b}")
print(f"除法: {a} / {b} = {a / b}")  # 浮点除法
print(f"整除: {a} // {b} = {a // b}")  # 整数除法
print(f"取余: {a} % {b} = {a % b}")
print(f"幂运算: {a} ** {b} = {a ** b}")

# 比较运算符
x = 5
y = 10
print(f"{x} == {y}: {x == y}")
print(f"{x} != {y}: {x != y}")
print(f"{x} > {y}: {x > y}")
print(f"{x} < {y}: {x < y}")
print(f"{x} >= {y}: {x >= y}")
print(f"{x} <= {y}: {x <= y}")

# 逻辑运算符
p = True
q = False
print(f"p and q: {p and q}")
print(f"p or q: {p or q}")
print(f"not p: {not p}")
# 短路特性演示
print(True or 1/0)  # 不会执行1/0
print(False and 1/0)  # 不会执行1/0

# 位运算符
a = 60  # 二进制 0011 1100
b = 13  # 二进制 0000 1101
print(f"按位与 &: {a & b}")    # 0000 1100
print(f"按位或 |: {a | b}")    # 0011 1101
print(f"按位异或 ^: {a ^ b}")  # 0011 0001
print(f"按位取反 ~: {~a}")     # 1100 0011
print(f"左移 <<: {a << 2}")    # 1111 0000
print(f"右移 >>: {a >> 2}")    # 0000 1111

# 格式化输出 重点
# f-strings
# 格式化数字
pi = 3.1415926
print(f"π = {pi:.2f}")  # 保留2位小数
print(f"π = {pi:.4f}")  # 保留4位小数
# 数字补零
number = 5
print(f"数字补零：{number:03d}")  # 补0 宽度为三 十进制

# print()高级特性
# 1. 不换行输出
print("Hello", end=" ")
print("World!")  # 输出：Hello World!
# 2. 分隔符
print("a", "b", "c", sep="-")  # 输出：a-b-c
# 3. 输出到文件
with open("/output.txt", "w") as f:
    print("Hello, File!", file=f)
# 4. 禁用自动换行
print("Line 1", end="")
print("Line 2")  # 输出：Line 1Line 2

# 综合练习-简易计算器
num1 = float(input('输入数字1:'))
num2 = float(input('输入数字2:'))
print('计算结果')
print(f"{num1} + {num2} = {num1 + num2}")
print(f"{num1} - {num2} = {num1 - num2}")
print(f"{num1} × {num2} = {num1 * num2}")
print(f"{num1} ÷ {num2} = {num1 / num2}")
