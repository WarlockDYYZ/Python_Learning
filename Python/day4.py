from functools import reduce
import time
import math


# 函数基础与高级特性
# 4.1 函数定义与参数传递
# 复习要点
# - 函数定义语法和参数类型（位置参数、默认参数、可变参数）
# - 参数传递机制（值传递 vs 引用传递）
# - 函数返回值的多种形式

# # 基本函数定义
# def 函数名(参数列表):
#     """函数文档字符串（可选）"""
#     函数体
#     [return 返回值]  # 可选，无return默认返回None

# 参数类型详解
# 位置参数：必须按顺序传入，数量和位置需与形参完全匹配
def student_info(name: str, age: int):
    print(f"Name: {name}, Age: {age}")


student_info("Alice", 20)  # 正确：按位置传入


# 下面虽然参数位置错误，但还是会正常输出
# Python 的类型注解（:str / :int）只是「提示」，不是「强制规定」！
# 它不会阻止你传错类型
# 它不会报错
# 它只会提醒你（编辑器里标黄），但代码照样运行
############################################
# student_info(20, "Alice")  # 错误：位置颠倒 #
############################################


# 默认参数：定义时指定默认值，调用时可省略
def student_info(name, age=18):  # age是默认参数
    print(f"Name: {name}, Age: {age}")


student_info("Bob")  # 输出：Name: Bob, Age: 18
student_info("Bob", 20)  # 输出：Name: Bob, Age: 20


# 注意：默认参数必须放在位置参数之后，且避免使用可变对象作为默认值


# 可变位置参数（*args）：接收任意数量的位置参数，在函数内部以元组形式存储
def sum_numbers(*args):
    return sum(args)


print(sum_numbers(1, 2, 3))  # 输出：6
print(sum_numbers(10, 20))  # 输出：30


# 可变关键字参数（kwargs）：接收任意数量的关键字参数，以字典形式存储
def print_info(**kwargs):
    for k, v in kwargs.items():
        print(f"{k}: {v}")


print_info(name="Alice", age=20, sex="female")


# 参数组合顺序：必须按以下顺序定义
def func(a, b=10, *args, **kwargs):
    print(f"位置参数: {a}")
    print(f"默认参数: {b}")
    print(f"可变位置参数: {args}")
    print(f"可变关键字参数: {kwargs}")


func(1, 2, 3, 4, x=5, y=6)


# 练习题
# 练习
# 1：定义一个学生信息函数
# 定义一个函数print_student_info，接收学生姓名、年龄、性别、成绩（可选，默认60）
# 并打印学生的基本信息和成绩等级（90+优秀，80-89良好，70-79中等，60-69及格，60以下不及格）
def print_student_info(name, age, gender, score=60):
    # 计算成绩等级
    if score >= 90:
        level = "优秀"
    elif score >= 80:
        level = "良好"
    elif score >= 70:
        level = "中等"
    elif score >= 60:
        level = "及格"
    else:
        level = "不及格"

    # 打印信息
    print(f"学生姓名：{name}")
    print(f"年龄：{age}岁")
    print(f"性别：{gender}")
    print(f"成绩：{score}分（等级：{level}）")


# 调用示例
print_student_info("张三", 18, "男", 85)
print_student_info("李四", 17, "女")  # 使用默认成绩60


# 练习
# 2：定义一个数学运算函数
# 定义一个函数math_operation，接收一个操作符（+、-、*、/）和多个数字
# 根据操作符对所有数字进行相应运算并返回结果
def math_operation(operator, *numbers):
    if len(numbers) < 2:
        raise ValueError("至少需要两个数字进行运算")

    result = numbers[0]
    for num in numbers[1:]:
        if operator == '+':
            result += num
        elif operator == '-':
            result -= num
        elif operator == '*':
            result *= num
        elif operator == '/':
            if num == 0:
                raise ValueError("除数不能为0")
            result /= num
        else:
            raise ValueError("不支持的操作符")

    return result


# 调用示例
print(math_operation('+', 1, 2, 3, 4, 5))  # 输出：15
print(math_operation('*', 2, 3, 4))  # 输出：24
print(math_operation('-', 10, 3, 2))  # 输出：5
print(math_operation('/', 10, 2))  # 输出：5.0


# 练习
# 3：定义一个统计函数
# 定义一个函数statistics，接收一个数字列表和一个操作（max、min、avg、sum）
# 返回相应的统计结果
def statistics(numbers, operation):
    if not numbers:
        raise ValueError("列表不能为空")
    if operation == 'max':
        return max(numbers)
    elif operation == 'min':
        return min(numbers)
    elif operation == 'avg':
        return sum(numbers) / len(numbers)
    elif operation == 'sum':
        return sum(numbers)
    else:
        raise ValueError("不支持的操作")


# 调用示例
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(statistics(nums, 'max'))  # 输出：10
print(statistics(nums, 'min'))  # 输出：1
print(statistics(nums, 'avg'))  # 输出：5.5
print(statistics(nums, 'sum'))  # 输出：55
print("*" * 50)

# 4.2
# Lambda表达式与匿名函数
# Lambda表达式基础
# 基本语法：lambda 参数列表: 表达式

# 示例：计算平方
# 不要把 lambda 表达式赋值给变量，应该用普通的 def 函数
# PEP 8 禁止这么写
# lambda 设计初衷：用于临时、简短的匿名函数，比如给 map/reduce/sort 用
# 赋值给变量后：失去了匿名意义，还不如普通函数清晰
# 调试更差：lambda 没有函数名，报错时栈信息不友好
# 代码风格规范：PEP 8 明确要求有名字的函数用 def
square = lambda x: x ** 2  # 不建议该操作，仅作为实例演示
print(square(5))  # 输出：25
print("*" * 50)

# 作为参数传递（如排序）
students = [("Alice", 20), ("Bob", 18)]
# 按年龄排序，默认升序
students_sorted = sorted(students, key=lambda x: x[1])
print(students_sorted)  # 输出：[('Bob', 18), ('Alice', 20)]
print("*" * 50)

# Lambda表达式特点
# - 匿名性：无函数名，仅临时使用
# - 单行性：仅含一个表达式，无法包含复杂逻辑
# - 返回值：自动返回表达式结果，无需return
# - 适用场景：简单逻辑、作为高阶函数参数（如sorted()、map()、filter()）

# 常用高阶函数与Lambda配合
# map()函数：对可迭代对象中的每个元素应用函数
numbers = [1, 2, 3, 4, 5]
squares = map(lambda x: x ** 2, numbers)
print(list(squares))  # 输出：[1, 4, 9, 16, 25]
print("*" * 50)

# filter()函数：过滤符合条件的元素
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = filter(lambda x: x % 2 == 0, numbers)
print(list(even_numbers))  # 输出：[2, 4, 6, 8, 10]
print("*" * 50)

# reduce()函数（需导入functools）：对元素进行累积操作
numbers = [1, 2, 3, 4, 5]
product = reduce(lambda x, y: x * y, numbers)
# # reduce = 归约 / 累积计算
# # 它会把列表里的元素，两个两个依次计算，最后合并成一个结果
# # 第 1 步：x=1，y=2 → 1×2 = 2
# # 第 2 步：x=2，y=3 → 2×3 = 6
# # 第 3 步：x=6，y=4 → 6×4 = 24
# # 第 4 步：x=24，y=5 → 24×5 = 120
print(product)  # 输出：120
print("*" * 50)

# 练习题
# 使用 Lambda 进行数据处理
# 1. 定义一个Lambda函数，计算两个数的平均值
avg = lambda x, y: (x + y) / 2
print(avg(5, 7))  # 输出：6.0
print("*" * 50)

# 2. 使用map()和Lambda计算列表中每个数的立方
numbers = [1, 2, 3, 4, 5]
cubes = map(lambda x: x ** 3, numbers)
print(list(cubes))  # 输出：[1, 8, 27, 64, 125]
print("*" * 50)

# 3. 使用filter()和Lambda筛选出能被3整除的数
numbers = list(range(1, 21))
divisible_by_3 = filter(lambda x: x % 3 == 0, numbers)
print(list(divisible_by_3))  # 输出：[3, 6, 9, 12, 15, 18]
print("*" * 50)

# 4. 使用reduce()和Lambda计算1到100的和
sum_1_to_100 = reduce(lambda x, y: x + y, range(1, 101))
print(sum_1_to_100)  # 输出：5050
print("*" * 50)

# 练习Lambda在排序中的应用
# 1. 对字典列表按年龄排序
people = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35}
]
people_sorted_by_age = sorted(people, key=lambda x: x["age"])
print(people_sorted_by_age)  # 按年龄升序
print("*" * 50)

# 2. 对元组列表按第二个元素降序排序
tuples = [(1, 3), (2, 2), (3, 1)]
# sorted(iterable, key=None, reverse=False)
# reverse（可选，默认 False）,False → 升序（从小到大）True → 降序（从大到小）
# 作用：对序列排序，返回一个新的排好序的列表
# 不会修改原数据，和列表的 .sort() 不一样
tuples_sorted = sorted(tuples, key=lambda x: x[1], reverse=True)
print(tuples_sorted)  # 按第二个元素降序
print("*" * 50)

# 3. 对字符串列表按长度排序
strings = ["apple", "banana", "cherry", "date"]
strings_sorted = sorted(strings, key=lambda x: len(x))
print(strings_sorted)  # 按长度升序
print("*" * 50)

# 练习Lambda表达式
# Lambda函数，匿名很重要，以下仅用于学习演示
# 1. 定义一个Lambda，判断一个数是否为偶数
is_even = lambda x: x % 2 == 0
print(is_even(4))  # 输出：True
print(is_even(5))  # 输出：False
print("*" * 50)
#    # 2. 定义一个Lambda，判断一个年份是否为闰年
is_leap_year = lambda year: year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
print(is_leap_year(2020))  # 输出：True
print(is_leap_year(2021))  # 输出：False
print("*" * 50)
#    # 3. 定义一个Lambda，计算BMI（身体质量指数）
bmi_calculator = lambda weight, height: weight / (height ** 2)
print(bmi_calculator(70, 1.75))  # 输出：22.857...
print("*" * 50)


# 4.3
# 函数高级特性
# 复习要点
# - 装饰器的定义和使用
# - 生成器与迭代器的原理和应用
# - 函数的嵌套定义和闭包
# 装饰器基础: 装饰器本质是一个高阶函数，接受函数作为参数并返回新函数
def decorator(func):
    def wrapper(*args, **kwargs):
        # 在调用原函数前执行的代码
        print("装饰器开始执行")
        result = func(*args, **kwargs)
        # 在调用原函数后执行的代码
        print("装饰器执行结束")
        return result

    return wrapper


# 使用装饰器
@decorator
def say_hello(name):
    print(f"Hello, {name}!")
    return "Hello"


say_hello("Alice")
print("*" * 50)


# 生成器与迭代器
# 生成器是一种可以按需逐个产生值、而不是一次性创建所有值的迭代器
# 它使用 yield 关键字返回数据，暂停并保留函数状态，下次调用时从暂停处继续执行
# 核心特点
# 占用内存极小：一边循环一边生成，不把所有结果存在内存里
# 惰性计算：只有迭代到它时才计算下一个值
# 是迭代器，可以用 for 遍历、next() 获取下一个值
# 函数中只要有 yield，就是生成器函数

# 生成器函数：使用yield关键字
def generator_function():
    yield 1
    yield 2
    yield 3


# 创建生成器对象
gen = generator_function()
print(next(gen))  # 输出：1
print(next(gen))  # 输出：2
print(next(gen))  # 输出：3
print("*" * 50)

# 生成器表达式
gen_expression = (x for x in range(1, 10) if x % 2 == 0)
print(list(gen_expression))  # 输出：[2, 4, 6, 8]
print("*" * 50)


# 闭包应用
# 闭包就是：函数嵌套函数时，内层函数引用了外层函数的变量，并且外层函数把内层函数返回出去，这样就形成了闭包
# 函数 + 它引用的外部环境变量 → 捆绑在一起 = 闭包
# 外部函数已经执行完，外部函数中变量也不会被销毁
# 这种带着环境一起带走的函数，就是闭包
# 闭包有什么用
# 1. 保留状态,比如计数器，不用全局变量也能记住当前数字。
# 2. 装饰器的底层就是闭包
# def decorator(func):
#     def wrapper():
#         ...
#     return wrapper
# 这就是标准闭包：wrapper 引用了外层 func
# 3. 避免全局变量污染

# 闭包示例：计算移动平均值
def moving_average():
    values = []

    def calculate_average(new_value):
        values.append(new_value)
        return sum(values) / len(values)

    return calculate_average


# 创建闭包实例
avg_calculator = moving_average()
print(avg_calculator(10))  # 输出：10.0
print(avg_calculator(20))  # 输出：15.0
print(avg_calculator(30))  # 输出：20.0
print("*" * 50)


# 练习
# 7：创建装饰器
# 1. 创建一个计时装饰器，计算函数执行时间


def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} 执行时间：{end_time - start_time:.4f}秒")
        return result

    return wrapper


# 使用装饰器
@timer_decorator
def heavy_function(n):
    result = 0
    for i in range(n):
        result += i
    return result


print(heavy_function(1000000))  # 计算1到100万的和
print("*" * 50)


# 2. 创建一个日志装饰器，记录函数调用信息
def logger_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"调用函数：{func.__name__}")
        print(f"参数：args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"返回值：{result}")
        return result

    return wrapper


@logger_decorator
def add(a, b):
    return a + b


@logger_decorator
def multiply(a, b, c=1):
    return a * b * c


add(3, 5)
multiply(2, 3, 4)
print("*" * 50)


# 练习
# 8：生成器应用
# 1. 创建一个斐波那契数列生成器
def fibonacci_generator():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


#    # 使用生成器
fib_gen = fibonacci_generator()
for _ in range(10):
    print(next(fib_gen), end=" ")  # 输出：0 1 1 2 3 5 8 13 21 34
print("\n" + "*" * 50)


# 2. 创建一个质数生成器
def prime_generator():
    # 第一个返回值就是
    # 2（唯一的偶质数）
    # 执行到这里，函数暂停，把
    # 2
    # 抛出去
    # 下次调用再从这里继续往下走
    yield 2  # 2是最小的质数
    candidate = 3
    while True:
        is_prime = True
        for i in range(2, int(candidate ** 0.5) + 1):
            if candidate % i == 0:
                is_prime = False
                break
        # 是质数 → 用yield 返回, 作用类似return
        # 函数暂停，等待下次调用
        if is_prime:
            yield candidate
        candidate += 2  # 只检查奇数


# 使用质数生成器
prime_gen = prime_generator()
for _ in range(10):
    print(next(prime_gen), end=" ")  # 输出前10个质数
print("\n" + "*" * 50)


# 3. 使用生成器处理大文件
def read_large_file(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            yield line.strip()


# 模拟大文件处理, 没有这个文件
# for line in read_large_file('large_file.txt'):
#     print(line)  # 逐行处理，不占用大量内存
# print("*" * 50)


# 练习
# 9：闭包和函数嵌套
# 1. 使用闭包创建计数器
def counter():
    count = 0

    def increment():
        nonlocal count  # 使用nonlocal关键字修改外部变量
        count += 1
        return count

    return increment


# 创建计数器实例
counter1 = counter()
print(counter1())  # 输出：1
print(counter1())  # 输出：2
print(counter1())  # 输出：3
print("*" * 50)


# 2. 函数嵌套示例：创建数学函数
def create_math_function(operation):
    def add(a, b):
        return a + b

    def multiply(a, b):
        return a * b

    def subtract(a, b):
        return a - b

    if operation == '+':
        return add
    elif operation == '*':
        return multiply
    elif operation == '-':
        return subtract


# 创建不同的数学函数
add_func = create_math_function('+')
multiply_func = create_math_function('*')
subtract_func = create_math_function('-')
# 返回函数本身，函数需要两个参数
print(add_func(5, 3))  # 输出：8
print(multiply_func(4, 6))  # 输出：24
print(subtract_func(10, 7))  # 输出：3
print("*" * 50)


# 面向对象编程基础
# 5.1 类与对象
# 复习要点
# - 类的定义和对象实例化
# - 构造方法__init__和析构方法__del__
# - 实例属性和类属性的区别
# - 实例方法、类方法和静态方法


# 类定义基础
# 定义一个Person类
class Person:
    # 类属性
    species = "人类"

    # 构造方法
    def __init__(self, name, age, gender):
        # 实例属性
        self.name = name
        self.age = age
        self.gender = gender

    # 实例方法
    def eat(self, food):
        print(f"{self.name}正在吃{food}")

    def work(self):
        print(f"{self.name}正在工作")

    # 类方法
    @classmethod
    def change_species(cls, new_species):
        cls.species = new_species

    # 静态方法
    @staticmethod
    def is_adult(age):
        return age >= 18


# 对象实例化与使用
# 创建对象
person1 = Person("张三", 25, "男")
person2 = Person("李四", 30, "女")
# 访问实例属性
print(person1.name)  # 输出：张三
print(person2.age)  # 输出：30
# 调用实例方法
person1.eat("米饭")  # 输出：张三正在吃米饭
person2.work()  # 输出：李四正在工作
# 访问类属性
print(Person.species)  # 输出：人类
print(person1.species)  # 输出：人类（对象也可访问类属性）
# 调用类方法
Person.change_species("智人")
print(Person.species)  # 输出：智人
# 调用静态方法
print(Person.is_adult(25))  # 输出：True
print(Person.is_adult(17))  # 输出：False
print("*" * 50)


# 练习题
# 练习
# 1：定义学生类
# 定义一个Student类，包含以下属性和方法：
# 属性：姓名(name)、年龄(age)、学号(student_id)、成绩(score)
# 方法：
# - __init__: 初始化属性
# - get_info: 返回学生基本信息字符串
# - set_score: 设置成绩（需检查成绩是否在0-100范围内）
# - get_grade: 返回成绩等级（90+优秀，80-89良好，70-79中等，60-69及格，60以下不及格）
# - is_passed: 判断是否及格
class Student:
    def __init__(self, name, age, student_id):
        self.name = name
        self.age = age
        self.student_id = student_id
        self.score = 0  # 默认成绩为0

    def get_info(self):
        return f"姓名：{self.name}，年龄：{self.age}岁，学号：{self.student_id}，成绩：{self.score}分"

    def set_score(self, score):
        if 0 <= score <= 100:
            self.score = score
        else:
            raise ValueError("成绩必须在0-100分之间")

    def get_grade(self):
        if self.score >= 90:
            return "优秀"
        elif self.score >= 80:
            return "良好"
        elif self.score >= 70:
            return "中等"
        elif self.score >= 60:
            return "及格"
        else:
            return "不及格"

    def is_passed(self):
        return self.score >= 60


# 创建学生对象并测试
stu1 = Student("王五", 18, "2026001")
stu1.set_score(85)
print(stu1.get_info())  # 输出：姓名：王五，年龄：18岁，学号：2026001，成绩：85分
print(f"成绩等级：{stu1.get_grade()}")  # 输出：良好
print(f"是否及格：{'是' if stu1.is_passed() else '否'}")  # 输出：是
stu2 = Student("赵六", 17, "2026002")
stu2.set_score(55)
print(stu2.get_info())  # 输出：姓名：赵六，年龄：17岁，学号：2026002，成绩：55分
print(f"成绩等级：{stu2.get_grade()}")  # 输出：不及格
print(f"是否及格：{'是' if stu2.is_passed() else '否'}")  # 输出：否
print("*" * 50)


# 练习
# 2：定义几何图形类
# 定义一个Circle类（圆形）：
# 属性：半径(radius)
# 方法：
# - __init__: 初始化半径
# - get_area: 计算面积
# - get_circumference: 计算周长
# 定义一个Rectangle类（矩形）：
# 属性：长(length)、宽(width)
# 方法：
# - __init__: 初始化长和宽
# - get_area: 计算面积
# - get_perimeter: 计算周长
class Circle:
    def __init__(self, radius):
        self.radius = radius

    def get_area(self):
        return math.pi * self.radius ** 2

    def get_circumference(self):
        return 2 * math.pi * self.radius


class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def get_area(self):
        return self.length * self.width

    def get_perimeter(self):
        return 2 * (self.length + self.width)


# 测试代码
circle = Circle(5)
print(f"圆的面积：{circle.get_area():.2f}")  # 输出：78.54
print(f"圆的周长：{circle.get_circumference():.2f}")  # 输出：31.42
rectangle = Rectangle(6, 4)
print(f"矩形的面积：{rectangle.get_area()}")  # 输出：24
print(f"矩形的周长：{rectangle.get_perimeter()}")  # 输出：20
print("*" * 50)


# 练习
# 3：定义银行账户类
# 定义一个BankAccount类：
# 属性：账号(account_number)、余额(balance)、客户姓名(customer_name)
# 方法：
# - __init__: 初始化属性（余额默认0）
# - deposit: 存款（增加余额）
# - withdraw: 取款（减少余额，不能透支）
# - get_balance: 获取当前余额
# - get_account_info: 返回账户信息
class BankAccount:
    def __init__(self, account_number, customer_name, balance=0):
        self.account_number = account_number
        self.customer_name = customer_name
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"存入{amount}元，当前余额：{self.balance}元")
        else:
            print("存款金额必须大于0")

    def withdraw(self, amount):
        if amount > 0:
            if self.balance >= amount:
                self.balance -= amount
                print(f"取出{amount}元，当前余额：{self.balance}元")
            else:
                print("余额不足，无法取款")
        else:
            print("取款金额必须大于0")

    def get_balance(self):
        return self.balance

    def get_account_info(self):
        return f"账户名：{self.customer_name}，账号：{self.account_number}，余额：{self.balance}元"


# 创建账户并操作
account = BankAccount("6228480000000000000", "张三", 1000)
print(account.get_account_info())  # 输出账户信息
account.deposit(500)  # 存入500
account.withdraw(300)  # 取出300
account.withdraw(2000)  # 余额不足，无法取出
print(f"当前余额：{account.get_balance()}元")  # 输出：1200
print("*" * 50)


# 5.2 继承与多态
# 复习要点
# - 单继承和多继承的语法
# - 方法重写（Override）
# - super()函数的使用
# - 多态的实现和应用

# 继承基础
# 父类（基类）
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name}发出声音")


# 子类（派生类）继承Animal类
class Dog(Animal):
    def speak(self):  # 重写父类方法
        print(f"{self.name}汪汪叫")


class Cat(Animal):
    def speak(self):  # 重写父类方法
        print(f"{self.name}喵喵叫")


# 创建子类对象
dog = Dog("大黄")
cat = Cat("小白")
# 调用speak方法（多态体现）
dog.speak()  # 输出：大黄汪汪叫
cat.speak()  # 输出：小白喵喵叫


# 多继承示例
class Flyable:
    @staticmethod
    def fly():
        print("我会飞")


class Swimmable:
    @staticmethod
    def swim():
        print("我会游泳")


# 企鹅类继承Flyable和Swimmable
class Penguin(Flyable, Swimmable):
    @staticmethod
    def walk():
        print("我会走路")


# 创建企鹅对象
penguin = Penguin()
penguin.fly()  # 输出：我会飞, 企鹅应该不会飞
penguin.swim()  # 输出：我会游泳
penguin.walk()  # 输出：我会走路

# super()函数使用
#    # 父类
# class Parent:
#     def __init__(self, value):
#          self.value = value
#          print(f"Parent初始化，value = {value}")
#    # 子类
# class Child(Parent):
#     def __init__(self, value, extra):
#          super().__init__(value)  # 调用父类的__init__方法
#          self.extra = extra
#          print(f"Child初始化，extra = {extra}")
#    # 创建子类对象
# child = Child(10, "额外信息")
# print(f"value = {child.value}, extra = {child.extra}")
# 练习题
# 练习
# 4：员工继承体系
#    # 定义一个Employee类（员工）：
#    # 属性：姓名(name)、工号(employee_id)、部门(department)
#    # 方法：
#    # - __init__: 初始化属性
#    # - work: 打印"员工在工作"
#    # 定义一个Manager类（经理），继承自Employee：
#    # 新增属性：管理的员工列表(managed_employees)
#    # 重写work方法：打印"经理在管理"，并调用每个下属的work方法
#    # 定义一个Developer类（开发者），继承自Employee：
#    # 新增属性：编程语言(programming_language)
#    # 重写work方法：打印"开发者在编写代码"
# class Employee:
#     def __init__(self, name, employee_id, department):
#          self.name = name
#          self.employee_id = employee_id
#          self.department = department
#
#     def work(self):
#          print(f"{self.name}（工号：{self.employee_id}）在工作")
# class Manager(Employee):
#     def __init__(self, name, employee_id, department, managed_employees=[]):
#          super().__init__(name, employee_id, department)
#          self.managed_employees = managed_employees
#
#     def work(self):
#          print(f"{self.name}（经理）在管理")
#          for employee in self.managed_employees:
#                employee.work()
# class Developer(Employee):
#     def __init__(self, name, employee_id, department, programming_language):
#          super().__init__(name, employee_id, department)
#          self.programming_language = programming_language
#
#     def work(self):
#          print(f"{self.name}（开发者）在编写{self.programming_language}代码")
#    # 创建员工对象
# dev1 = Developer("张三", "001", "研发部", "Python")
# dev2 = Developer("李四", "002", "研发部", "Java")
# manager = Manager("王五", "003", "研发部", [dev1, dev2])
#    # 调用work方法（多态体现）
# dev1.work()  # 输出：张三（开发者）在编写Python代码
# dev2.work()  # 输出：李四（开发者）在编写Java代码
# manager.work()  # 输出：王五（经理）在管理，然后调用两个开发者的work方法
# 练习
# 5：几何图形继承体系
#    # 定义一个Shape类（图形）：
#    # 方法：
#    # - get_area: 计算面积（抽象方法，抛出NotImplementedError）
#    # - get_perimeter: 计算周长（抽象方法，抛出NotImplementedError）
#    # 定义一个Rectangle类（矩形），继承自Shape：
#    # 属性：长(length)、宽(width)
#    # 重写get_area和get_perimeter方法
#    # 定义一个Square类（正方形），继承自Rectangle：
#    # 重写初始化方法，只需接收边长
#    # 定义一个Circle类（圆形），继承自Shape：
#    # 属性：半径(radius)
#    # 重写get_area和get_perimeter方法
# import math
# class Shape:
#     def get_area(self):
#          raise NotImplementedError("子类必须实现get_area方法")
#
#     def get_perimeter(self):
#          raise NotImplementedError("子类必须实现get_perimeter方法")
# class Rectangle(Shape):
#     def __init__(self, length, width):
#          self.length = length
#          self.width = width
#
#     def get_area(self):
#          return self.length * self.width
#
#     def get_perimeter(self):
#          return 2 * (self.length + self.width)
# class Square(Rectangle):
#     def __init__(self, side_length):
#          super().__init__(side_length, side_length)
# class Circle(Shape):
#     def __init__(self, radius):
#          self.radius = radius
#
#     def get_area(self):
#          return math.pi * self.radius ** 2
#
#     def get_perimeter(self):
#          return 2 * math.pi * self.radius
#    # 创建不同图形对象
# rect = Rectangle(6, 4)
# square = Square(5)
# circle = Circle(3)
#    # 多态调用
# shapes = [rect, square, circle]
# for shape in shapes:
#     print(f"面积：{shape.get_area():.2f}，周长：{shape.get_perimeter():.2f}")
# 练习
# 6：动物继承体系
#    # 定义一个Animal类（动物）：
#    # 属性：名称(name)、年龄(age)
#    # 方法：
#    # - __init__: 初始化属性
#    # - eat: 打印"动物在吃东西"
#    # - sleep: 打印"动物在睡觉"
#    # 定义一个Bird类（鸟类），继承自Animal：
#    # 新增属性：是否会飞(can_fly)
#    # 重写eat方法：打印"鸟类在啄食"
#    # 新增方法：fly: 打印"鸟类在飞翔"
#    # 定义一个Fish类（鱼类），继承自Animal：
#    # 新增属性：生活环境(habitat)
#    # 重写eat方法：打印"鱼类在觅食"
#    # 新增方法：swim: 打印"鱼类在游泳"
# class Animal:
#     def __init__(self, name, age):
#          self.name = name
#          self.age = age
#
#     def eat(self):
#          print(f"{self.name}（{self.age}岁）在吃东西")
#
#     def sleep(self):
#          print(f"{self.name}（{self.age}岁）在睡觉")
# class Bird(Animal):
#     def __init__(self, name, age, can_fly=True):
#          super().__init__(name, age)
#          self.can_fly = can_fly
#
#     def eat(self):
#          print(f"{self.name}（鸟）在啄食")
#
#     def fly(self):
#          if self.can_fly:
#                print(f"{self.name}在天空飞翔")
#          else:
#                print(f"{self.name}不会飞")
# class Fish(Animal):
#     def __init__(self, name, age, habitat):
#          super().__init__(name, age)
#          self.habitat = habitat
#
#     def eat(self):
#          print(f"{self.name}（鱼）在觅食")
#
#     def swim(self):
#          print(f"{self.name}在{self.habitat}中游泳")
#    # 创建动物对象
# bird1 = Bird("麻雀", 2)
# bird2 = Bird("企鹅", 3, False)
# fish1 = Fish("金鱼", 1, "鱼缸")
# fish2 = Fish("鲨鱼", 5, "海洋")
#    # 多态调用
# animals = [bird1, bird2, fish1, fish2]
# for animal in animals:
#     animal.eat()
#     animal.sleep()
#     if isinstance(animal, Bird):
#          animal.fly()
#     elif isinstance(animal, Fish):
#          animal.swim()
#     print()
# 5.3
# 封装与特殊方法（30
# 分钟）
# 复习要点
# - 私有属性和公有属性的定义
# - @ property装饰器的使用
# - 特殊方法（魔术方法）的重载
# 封装示例
#    # 封装示例：学生类
# class Student:
#     def __init__(self, name, age):
#          self.name = name  # 公有属性
#          self._age = age    # 受保护属性
#          self.__score = 0  # 私有属性（双下划线）
#
#     def get_score(self):
#          return self.__score
#
#     def set_score(self, score):
#          if 0 <= score <= 100:
#                self.__score = score
#          else:
#                raise ValueError("成绩必须在0-100分之间")
#    # 创建学生对象
# stu = Student("张三", 18)
# stu.set_score(85)
# print(stu.get_score())  # 输出：85
# print(stu._age)  # 可以访问，但不建议
#    # print(stu.__score)      # 无法直接访问，会报错
# 特殊方法示例
#    # 特殊方法示例：向量类
# class Vector:
#     def __init__(self, x, y):
#          self.x = x
#          self.y = y
#
#     def __add__(self, other):  # 重载加法操作符
#          return Vector(self.x + other.x, self.y + other.y)
#
#     def __sub__(self, other):  # 重载减法操作符
#          return Vector(self.x - other.x, self.y - other.y)
#
#     def __str__(self):  # 重载str()方法
#          return f"({self.x}, {self.y})"
#
#     def __len__(self):  # 重载len()方法
#          return int((self.x**2 + self.y**2) ** 0.5)
#    # 使用向量类
# v1 = Vector(3, 4)
# v2 = Vector(1, 2)
# v3 = v1 + v2  # 等价于 v1.__add__(v2)
# v4 = v1 - v2  # 等价于 v1.__sub__(v2)
# print(v3)  # 输出：(4, 6)
# print(v4)  # 输出：(2, 2)
# print(len(v1))  # 输出：5（向量长度）
# 练习题
# 练习
# 7：使用 @ property
# 装饰器
#    # 定义一个Temperature类：
#    # 属性：
#    # - 华氏温度(fahrenheit)
#    # - 摄氏温度(celsius) - 使用@property装饰器实现
#    # 方法：
#    # - 初始化时可以传入华氏温度或摄氏温度
#    # - 提供温度转换功能
# class Temperature:
#     def __init__(self, value, unit='c'):
#          if unit == 'c':
#                self._celsius = value
#          else:
#                self._celsius = (value - 32) * 5/9
#
#     @property
#     def celsius(self):
#          return self._celsius
#
#     @celsius.setter
#     def celsius(self, value):
#          self._celsius = value
#
#     @property
#     def fahrenheit(self):
#          return self._celsius * 9/5 + 32
#
#     @fahrenheit.setter
#     def fahrenheit(self, value):
#          self._celsius = (value - 32) * 5/9
#    # 创建温度对象
# temp1 = Temperature(25, 'c')  # 25摄氏度
# temp2 = Temperature(77, 'f')  # 77华氏度
# print(f"temp1: {temp1.celsius}°C = {temp1.fahrenheit}°F")
# print(f"temp2: {temp2.celsius}°C = {temp2.fahrenheit}°F")
#    # 修改温度
# temp1.fahrenheit = 86  # 设置为86华氏度
# print(f"修改后 temp1: {temp1.celsius}°C = {temp1.fahrenheit}°F")
# temp2.celsius = 30  # 设置为30摄氏度
# print(f"修改后 temp2: {temp2.celsius}°C = {temp2.fahrenheit}°F")
# 练习
# 8：实现一个分数类
#    # 定义一个Fraction类（分数）：
#    # 属性：分子(numerator)、分母(denominator)
#    # 方法：
#    # - __init__: 初始化分数（自动约分）
#    # - __str__: 返回分数的字符串表示
#    # - __add__: 重载加法操作符
#    # - __sub__: 重载减法操作符
#    # - __mul__: 重载乘法操作符
#    # - __truediv__: 重载除法操作符
#    # - 实现分数的比较操作（==, >, <等）
# class Fraction:
#     def __init__(self, numerator, denominator):
#          # 处理分母为0的情况
#          if denominator == 0:
#                raise ValueError("分母不能为0")
#
#          # 计算最大公约数并约分
#          gcd = self._gcd(numerator, denominator)
#          self.numerator = numerator // gcd
#          self.denominator = denominator // gcd
#
#     def _gcd(self, a, b):
#          # 计算最大公约数（欧几里得算法）
#          while b:
#                a, b = b, a % b
#          return a
#
#     def __str__(self):
#          if self.denominator == 1:
#                return f"{self.numerator}"
#          return f"{self.numerator}/{self.denominator}"
#
#     def __add__(self, other):
#          # 分数加法：通分后相加
#          new_denominator = self.denominator * other.denominator
#          new_numerator = (self.numerator * other.denominator +
#                                other.numerator * self.denominator)
#          return Fraction(new_numerator, new_denominator)
#
#     def __sub__(self, other):
#          # 分数减法：通分后相减
#          new_denominator = self.denominator * other.denominator
#          new_numerator = (self.numerator * other.denominator -
#                                other.numerator * self.denominator)
#          return Fraction(new_numerator, new_denominator)
#
#     def __mul__(self, other):
#          # 分数乘法：分子乘分子，分母乘分母
#          new_numerator = self.numerator * other.numerator
#          new_denominator = self.denominator * other.denominator
#          return Fraction(new_numerator, new_denominator)
#
#     def __truediv__(self, other):
#          # 分数除法：乘以倒数
#          new_numerator = self.numerator * other.denominator
#          new_denominator = self.denominator * other.numerator
#          return Fraction(new_numerator, new_denominator)
#
#     def __eq__(self, other):
#          return self.numerator == other.numerator and self.denominator == other.denominator
#
#     def __gt__(self, other):
#          # 比较分数大小：通分后比较分子
#          return self.numerator * other.denominator > other.numerator * self.denominator
#
#     def __lt__(self, other):
#          return self.numerator * other.denominator < other.numerator * self.denominator
#    # 创建分数对象
# frac1 = Fraction(1, 2)  # 1/2
# frac2 = Fraction(1, 3)  # 1/3
# print(f"{frac1} + {frac2} = {frac1 + frac2}")  # 输出：1/2 + 1/3 = 5/6
# print(f"{frac1} - {frac2} = {frac1 - frac2}")  # 输出：1/2 - 1/3 = 1/6
# print(f"{frac1} × {frac2} = {frac1  * frac2}")  # 输出：1/2 × 1/3 = 1/6
# print(f"{frac1} ÷ {frac2} = {frac1 / frac2}")  # 输出：1/2 ÷ 1/3 = 3/2
# print(f"{frac1} > {frac2}: {frac1 > frac2}")  # 输出：True
# print(f"{frac1} < {frac2}: {frac1 < frac2}")  # 输出：False
# print(f"{frac1} == {frac2}: {frac1 == frac2}")  # 输出：False
