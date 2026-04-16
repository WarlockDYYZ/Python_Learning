# 流程控制语句

# 条件判断（if-elif-else）
# 基本语法
x = 10
if x > 0:
    print(f"{x}是正数")
# if-else结构
x = -5
if x > 0:
    print(f"{x}是正数")
else:
    print(f"{x}是非正数")
# if-elif-else结构
x = 0
if x > 0:
    print(f"{x}是正数")
elif x < 0:
    print(f"{x}是负数")
else:
    print(f"{x}是零")

# 复合条件判断
# 多个条件组合
age = 25
score = 95
if age >= 18 and score >= 60:
    print("成年人且成绩合格")
if age < 18 or score < 60:
    print("未成年人或成绩不合格")
# 条件嵌套
if age >= 18:
    if score >= 90:
        print("优秀（A）")
    elif score >= 80:
        print("良好（B）")
    else:
        print("及格（C）")
else:
    print("未成年人，不参与评级")

# 条件表达式（C语言三元运算符）
# 语法：值1 if 条件 else 值2
x = 10
result = "正数" if x > 0 else "非正数"
print(result)  # 正数
# 多个条件表达式
score = 95
grade = "A" if score >= 90 else ("B" if score >= 80 else ("C" if score >= 60 else "D"))
print(f"成绩等级：{grade}")  # A

# 条件判断进阶
# Python 中，以下值被视为 False：
# False
# None
# 0（所有数字类型的零）
# 空序列（空字符串、空列表、空元组、空字典、空集合）
# 空 range 对象
# 其他值都被视为 True

# 真值测试示例
if "":
    print("空字符串为True")
else:
    print("空字符串为False")  # 输出
if []:
    print("空列表为True")
else:
    print("空列表为False")  # 输出
if 0:
    print("0为True")
else:
    print("0为False")  # 输出
if None:
    print("None为True")
else:
    print("None为False")  # 输出
if [1, 2, 3]:
    print("非空列表为True")  # 输出

# 链式比较
# 链式比较（相当于 0 <= score <= 100）
score = 95
if 0 <= score <= 100:
    print("成绩有效")
# 多个链式比较
a = 5
if 1 < a < 10:
    print(f"{a}在1和10之间")  # 输出

# 循环语句
# for 循环与迭代，用于遍历可迭代对象
# 基本语法
# 遍历列表
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
# 遍历字符串
s = "Hello"
for c in s:
    print(c)
# 遍历字典（键）
person = {"name": "Alice", "age": 30}
# 默认返回键，可通过键找到对应的值
for key in person:
    print(key)  # name, age
# 遍历字典（值）
for value in person.values():
    print(value)  # Alice, 30
# 遍历字典（键值对）
for key, value in person.items():
    print(f"{key}: {value}")  # name: Alice, age: 30

# range () 函数
# range(stop)：0到stop-1
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4
# range(start, stop)：start到stop-1
for i in range(1, 6):
    print(i)  # 1, 2, 3, 4, 5
# range(start, stop, step)：带步长
for i in range(0, 10, 2):
    print(i)  # 0, 2, 4, 6, 8
# 反向循环
for i in range(9, -1, -1):
    print(i)  # 9, 8, 7, ..., 0

# enumerate () 函数
# 同时获取索引和值
fruits = ["apple", "banana", "cherry"]
for index, fruit in enumerate(fruits):
    print(f"索引{index}：{fruit}")
# 自定义起始索引
for index, fruit in enumerate(fruits, 1):
    print(f"第{index}个：{fruit}")

# while循环用于条件满足时重复执行代码块
# 基本语法
# 简单while循环
i = 0
while i < 5:
    print(i)
    i += 1
# 计算1到100的和
total = 0
i = 1
while i <= 100:
    total += i
    i += 1
print(f"1到100的和：{total}")
# 无限循环（需用break退出）
# while True:
#     print("按Ctrl+C退出")

# 循环控制语句
# break：退出整个循环
i = 0
while True:
    print(i)
    i += 1
    if i >= 5:
        break
# continue：跳过本次循环
for i in range(1, 11):
    if i % 2 == 0:
        continue  # 跳过偶数
    print(i)  # 1, 3, 5, 7, 9
# else子句：循环正常结束时执行（未被break中断）
for i in range(5):
    print(i)
else:
    print("循环正常结束")  # 输出
for i in range(5):
    if i == 3:
        break
    print(i)
else:
    print("循环正常结束")  # 不输出（被break中断）

# 嵌套循环
# 九九乘法表
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}×{i}={i*j}", end="\t")
    print()  # 换行
# 二维列表遍历
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
for row in matrix:
    for col in row:
        print(col, end=" ")
    print()  # 换行
# 查找满足条件的数对
# 找出1-100中所有和为100的两个数
for i in range(1, 100):
    for j in range(i, 100):
        if i + j == 100:
            print(f"{i} + {j} = 100")

# 循环优化技巧
# 提前终止循环
# 查找第一个平方数大于100的数
for i in range(1, 20):
    if i ** 2 > 100:
        print(f"{i}的平方是{i**2}，大于100")
        break  # 找到后立即退出
# 双重循环中的优化
found = False
for i in range(10):
    if found:
        break
    for j in range(10):
        if i + j == 15:
            print(f"找到{i} + {j} = 15")
            found = True
            break  # 退出内层循环

# 使用生成器表达式
# 计算1-100的平方和（生成器表达式）
sum_of_squares = sum(x**2 for x in range(1, 101))
print(f"平方和：{sum_of_squares}")
# 找出列表中的偶数（生成器表达式）
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = (x for x in numbers if x % 2 == 0)
print(list(even_numbers))  # [2, 4, 6, 8, 10]

# 列表推导式与生成器
# 列表推导式是 Python 的一个强大特性，允许简洁地创建列表
# 基本语法
# [表达式 for 变量 in 可迭代对象]
squares = [x**2 for x in range(1, 11)]
print(f"平方数：{squares}")  # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
# [表达式 for 变量 in 可迭代对象 if 条件]
even_squares = [x**2 for x in range(1, 11) if x % 2 == 0]
print(f"偶数平方：{even_squares}")  # [4, 16, 36, 64, 100]
# [表达式 if 条件 else 表达式 for 变量 in 可迭代对象]
result = [x if x % 2 == 0 else -x for x in range(1, 11)]
print(f"结果：{result}")  # [-1, 2, -3, 4, -5, 6, -7, 8, -9, 10]

# 嵌套列表推导式
# 二维列表展平
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
flat_list = [num for row in matrix for num in row]
#           [num for row in matrix for num in row]
#            ↑    ↑_____________↑  ↑_________↑
#           输出      外层循环          内层循环
print(f"展平列表：{flat_list}")  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
# 笛卡尔积
colors = ["red", "green", "blue"]
sizes = ["S", "M", "L"]
products = [(color, size) for color in colors for size in sizes]
print(f"笛卡尔积：{products}")  # [('red', 'S'), ('red', 'M'), ..., ('blue', 'L')]

# 生成器表达式
# 生成器表达式与列表推导式类似，但返回的是生成器对象
# 生成器基础
# 生成器表达式
gen = (x**2 for x in range(1, 11))
print(gen)  # <generator object <genexps> at 0x...>
# 转换为列表
print(list(gen))  # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
# 惰性计算（节省内存）
large_gen = (x**2 for x in range(1, 1000001))  # 不会立即生成所有元素
print(next(large_gen))  # 1
print(next(large_gen))  # 4
# 生成器的优势：
# 内存高效：不存储所有元素
# 延迟计算：按需生成元素
# 适合处理大数据集
