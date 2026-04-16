import random

# 1. 判断一个数是否为闰年
# 闰年条件：能被4整除但不能被100整除，或能被400整除
# input输入是一样的
year = 2020
if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
    print(f"{year}年是润年")
else:
    print(f"{year}年是润年")

# 2. 成绩等级判断
# 90为“A”，10分一档
score = 95
if score >= 90:
    print(f"A")
elif score >= 80:
    print(f"B")
elif score >= 70:
    print(f"C")
elif score >= 60:
    print(f"D")
else:
    print(f"E")

# 3. 判断三角形类型
a = 3
b = 4
c = 5
if a + b > c and a + c > b and c + b > a:
    print(f"边{a} {b} {c}, 可以构成三角形")
    if a == b == c:
        print(f"等边三角形")
    if a ** 2 + b ** 2 == c ** 2:
        print(f"直角三角形")
    if a == b or b == c or c == a:
        print(f"等腰三角形")
    else:
        print(f"普通三角形")
else:
    print(f"边{a} {b} {c}, 不可以构成三角形")

# 循环综合练习
# 1. 计算1到100的和（for循环）
sum_for = 0
for i in range(100):
    sum_for += i + 1
print(sum_for)

# 2. 计算1到100的和（while循环）
sum_while = 0
i = 1
while i <= 100:
    sum_while += i
    i += 1
print(sum_while)

# 3. 找出100以内的所有质数
for i in range(2, 101):
    is_prime = True
    for j in range(2, int(i ** 0.5) + 1):
        if i % j == 0:
            is_prime = False
            break
    if is_prime:
        print(f"{i} is prime")

# 4. 打印菱形
n = 5
for i in range(n + 1):
    print((n - i) * " " + (i * 2 - 1) * "*")
for i in range(n, 0, -1):
    print((n - i) * " " + (i * 2 - 1) * "*")

# 5. 斐波那契数列（前20项）
fib = [0, 1]
for i in range(0, 18):
    fib.append(fib[i] + fib[i + 1])
print(fib)
print(len(fib))

# 作业 3：列表推导式与生成器练习
# 1. 生成1-100的平方列表
squares = [x ** 2 for x in range(1, 101)]
print(squares)
# 2. 找出1-100中能被3整除的数
squares = [x for x in range(1, 101) if x % 3 == 0]
print(squares)
# 3. 生成100个随机数（1-1000）
# 这里用 _ 是因为：循环变量不需要使用，只是占位
random_numbers = [random.randint(1, 1000) for _ in range(100)]
print(f"100个随机数（前5个）：{random_numbers[:5]}...")
# 4. 二维列表展平
matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]]
flat = [num for row in matrix for num in row]
print(flat)

# 5. 生成器表达式：计算1-1000000的立方和
# 注意：使用生成器表达式不会立即生成所有元素
# sum() 可以直接吃生成器，不需要先建列表
# 用列表：sum([x**2 ...]) → 先生成 100 万项列表，占内存
# 用生成器：sum(x**2 ...) → 一边算一边加，不加完不存内存
# Python 允许 sum、max、min、all、any 里省略括号
cube_sum = sum(x ** 3 for x in range(1, 1000001))
print(cube_sum)
# 补充
# 列表推导式：
#   一次性把所有结果算完
#   全部存到内存里
#   是一个实实在在的列表
# 生成器表达式：
#    不一次性算完
#   不占大量内存
#   只是一个生成规则
#   你要一个，它才算一个、给你一个
#   用完就丢，不保存所有数据

# 6. 找出列表中的最大值（不使用max()函数）
numbers = [5, 2, 8, 1, 9, 3]
max_num = numbers[0]
for i in range(1, len(numbers)):
    if numbers[i] > max_num:
        max_num = numbers[i]
print(max_num)

# 7. 列表去重、保留原来顺序
lst = [2, 1, 3, 2, 1, 5, 3]

# 1. 字典方法
# Python3.7 后字典保留插入顺序
# dict.fromkeys(lst) 把列表（或可迭代对象）里的元素，变成字典的「键 key」，字典键不重复
new_lst = list(dict.fromkeys(lst))
print(new_lst)  # [2, 1, 3, 5]

# 2. 集合方法
seen = set()
res = []
for x in lst:
    if x not in seen:
        seen.add(x)
        res.append(x)
print(res)

# 3. 列表推导式
# [表达式 for 变量 in 可迭代对象]
# [表达式 for 变量 in 可迭代对象 if 条件]
# [表达式 if 条件 else 表达式 for 变量 in 可迭代对象]
res = []
[res.append(x) for x in lst if x not in res]
print(res)
