# list

# 列表定义
# 定义空列表
empty_list = []
another_empty = list()
# 定义有元素的列表
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "two", 3.14, True]
nested = [1, [2, 3], [4, [5, 6]]]  # 嵌套列表

# 访问列表元素

print(fruits[0])  # 第一个元素：apple
print(fruits[1])  # 第二个元素：banana
print(fruits[-1])  # 最后一个元素：cherry
print(fruits[-2])  # 倒数第二个元素：banana
# 切片操作
print(fruits[1:3])  # 从索引1到索引3（不包含3）：['banana', 'cherry']
print(fruits[:2])  # 从开头到索引2（不包含2）：['apple', 'banana']
print(fruits[1:])  # 从索引1到末尾：['banana', 'cherry']
print(fruits[::2])  # 步长为2：['apple', 'cherry']
print(fruits[::-1])  # 反转列表：['cherry', 'banana', 'apple']

# 修改列表元素
# 修改单个元素
numbers[0] = 100
print(f"修改后：{numbers}")  # [100, 2, 3, 4, 5]
# 修改多个元素（切片赋值）
numbers[1:3] = [20, 30]
print(f"切片修改后：{numbers}")  # [100, 20, 30, 4, 5]
# 插入元素
numbers.insert(2, 25)  # 在索引2处插入25
print(f"插入后：{numbers}")  # [100, 20, 25, 30, 4, 5]

# 添加元素
fruits = ["apple", "banana"]
# append()：在末尾添加元素
fruits.append("cherry")
print(f"append后：{fruits}")  # ['apple', 'banana', 'cherry']
# extend()：扩展列表
fruits.extend(["orange", "grape"])
print(f"extend后：{fruits}")  # ['apple', 'banana', 'cherry', 'orange', 'grape']
# insert()：在指定位置插入
fruits.insert(1, "blueberry")
print(f"insert后：{fruits}")  # ['apple', 'blueberry', 'banana', 'cherry', 'orange', 'grape']
# 删除元素
fruits = ["apple", "banana", "cherry", "orange", "grape"]
# remove()：删除指定值
fruits.remove("banana")
print(f"remove后：{fruits}")  # ['apple', 'cherry', 'orange', 'grape']
# pop()：删除指定索引的元素（默认删除最后一个）
last = fruits.pop()
print(f"pop()后：{fruits}，弹出的元素：{last}")  # ['apple', 'cherry', 'orange']
# pop(index)：删除指定索引
second = fruits.pop(1)
print(f"pop(1)后：{fruits}，弹出的元素：{second}")  # ['apple', 'orange']
# del语句：删除指定索引或切片
del fruits[0]
print(f"del后：{fruits}")  # ['orange']
# 清空列表
fruits.clear()
print(f"clear后：{fruits}")  # []

# 查找与统计
fruits = ["apple", "banana", "cherry", "banana", "orange"]
# 查找元素位置
print(fruits.index("banana"))  # 1（第一个出现的位置）
# print(fruits.index("grape"))  # 不存在会报错
# 统计元素出现次数
print(fruits.count("banana"))  # 2
# 判断元素是否存在
print("cherry" in fruits)  # True
print("grape" in fruits)  # False

# 排序与反转
numbers = [5, 2, 8, 1, 9, 3]
# 排序（默认升序）
numbers.sort()
print(f"sort()后：{numbers}")  # [1, 2, 3, 5, 8, 9]
# 降序排序
numbers.sort(reverse=True)
print(f"sort(reverse=True)后：{numbers}")  # [9, 8, 5, 3, 2, 1]
# 反转列表
numbers.reverse()
print(f"reverse()后：{numbers}")  # [1, 2, 3, 5, 8, 9]
# 使用sorted()函数（返回新列表）
original = [5, 2, 8, 1, 9, 3]
sorted_list = sorted(original)
print(f"原始列表：{original}")  # [5, 2, 8, 1, 9, 3]
print(f"排序后的新列表：{sorted_list}")  # [1, 2, 3, 5, 8, 9]

# 列表推导式 ***重点***
# 基础语法：[表达式 for 变量 in 可迭代对象]
squares = [x ** 2 for x in range(1, 11)]
print(f"平方数：{squares}")  # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
# 带条件的列表推导式
even_squares = [x ** 2 for x in range(1, 11) if x % 2 == 0]
print(f"偶数平方：{even_squares}")  # [4, 16, 36, 64, 100]
# 双重循环
pairs = [(i, j) for i in range(1, 3) for j in range(1, 3)]
print(f"笛卡尔积：{pairs}")  # [(1, 1), (1, 2), (2, 1), (2, 2)]

# Dictionary
# 字典定义
# 定义空字典
empty_dict = {}
another_empty = dict()
# 定义有内容的字典
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York",
    "is_student": False
}
# 混合类型的键和值
mixed_dict = {
    1: "one",
    "two": 2,
    3.14: "pi",
    "list": [1, 2, 3]
}
# 嵌套字典
nested_dict = {
    "person": {
        "name": "Bob",
        "age": 25
    },
    "contact": {
        "email": "bob@example.com",
        "phone": "123-456-7890"
    }
}
# 通过键访问值
print(person["name"])  # Alice
print(person["age"])  # 30
print(person["city"])  # New York
# 使用get()方法（推荐，避免KeyError）
print(person.get("name"))  # Alice
print(person.get("email"))  # None（不存在时返回None）
print(person.get("email", "未提供"))  # 不存在时返回默认值
# 修改值
person["age"] = 31
print(f"修改后年龄：{person['age']}")  # 31
# 添加新键值对
person["email"] = "alice@example.com"
print(f"添加email后：{person}")
# 字典方法详解
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}
# keys()：获取所有键
print(person.keys())  # dict_keys(['name', 'age', 'city'])
print(list(person.keys()))  # ['name', 'age', 'city']
# values()：获取所有值
print(person.values())  # dict_values(['Alice', 30, 'New York'])
print(list(person.values()))  # ['Alice', 30, 'New York']
# items()：获取所有键值对（元组形式）
print(person.items())  # dict_items([('name', 'Alice'), ('age', 30), ('city', 'New York')])
print(list(person.items()))  # [('name', 'Alice'), ('age', 30), ('city', 'New York')]
# pop()：删除指定键并返回对应的值
age = person.pop("age")
print(f"删除age后：{person}，删除的值：{age}")  # {'name': 'Alice', 'city': 'New York'}
# popitem()：删除并返回一个任意的键值对（3.7+是按插入顺序）
key, value = person.popitem()
print(f"popitem()：{key} = {value}")  # city = New York
# update()：更新字典
person.update({
    "name": "Bob",  # 存在则更新
    "email": "bob@example.com"  # 不存在则添加
})
print(f"update后：{person}")  # {'name': 'Bob', 'email': 'bob@example.com'}
# fromkeys()：创建新字典
keys = ["a", "b", "c"]
default_value = 0
new_dict = dict.fromkeys(keys, default_value)
print(f"fromkeys创建的字典：{new_dict}")  # {'a': 0, 'b': 0, 'c': 0}
# 字典推导式
# 基础语法：{键表达式: 值表达式 for 变量 in 可迭代对象}
squares_dict = {x: x ** 2 for x in range(1, 11)}
print(f"平方数字典：{squares_dict}")  # {1: 1, 2: 4, 3: 9, ..., 10: 100}
# 条件筛选
even_squares_dict = {x: x ** 2 for x in range(1, 11) if x % 2 == 0}
print(f"偶数平方字典：{even_squares_dict}")  # {2: 4, 4: 16, 6: 36, 8: 64, 10: 100}
# 转换列表为字典
keys = ["a", "b", "c"]
values = [1, 2, 3]
zipped_dict = dict(zip(keys, values))
print(f"zip转换的字典：{zipped_dict}")  # {'a': 1, 'b': 2, 'c': 3}

# Tuple
# 元组基础
# 定义元组
empty_tuple = ()
single_element = (1,)  # 单个元素需要逗号
fruits = ("apple", "banana", "cherry")
mixed = (1, "two", 3.14, True)
# 访问元素（与列表相同）
print(fruits[0])  # apple
print(fruits[1:3])  # ('banana', 'cherry')
# 元组不可变，以下操作会报错
# fruits[0] = "grape"  # TypeError: 'tuple' object does not support item assignment

# 解包操作
# 基础解包
a, b, c = (1, 2, 3)
print(f"a={a}, b={b}, c={c}")  # a=1, b=2, c=3
# 交换变量
a, b = b, a
print(f"交换后：a={a}, b={b}")  # a=2, b=1


# 函数返回多个值
def get_coordinates():
    return 10, 20


x, y = get_coordinates()
print(f"坐标：x={x}, y={y}")  # x=10, y=20
# 忽略某些值（使用下划线）
a, _, c = (1, 2, 3)  # 忽略第二个值
print(f"a={a}, c={c}")  # a=1, c=3

# 优势
# 1. 不可变性保证数据安全
# 2. 可作为字典的键（列表不行）
# 3. 比列表更节省内存
# 4. 用于函数返回多个值

# Set
# 集合基础
# 定义集合
empty_set = set()  # 注意：{}表示空字典
fruits = {"apple", "banana", "cherry", "apple"}  # 自动去重
print(f"水果集合：{fruits}")  # {'apple', 'banana', 'cherry'}
# 常用操作
fruits.add("orange")  # 添加元素
print(f"添加后：{fruits}")  # {'apple', 'banana', 'cherry', 'orange'}
fruits.remove("banana")  # 删除元素
print(f"删除后：{fruits}")  # {'apple', 'cherry', 'orange'}
# 集合运算
set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}
print(f"交集：{set1 & set2}")    # {4, 5}
print(f"并集：{set1 | set2}")    # {1, 2, 3, 4, 5, 6, 7, 8}
print(f"差集：{set1 - set2}")    # {1, 2, 3}
print(f"对称差：{set1 ^ set2}")  # {1, 2, 3, 6, 7, 8}
# 判断子集和超集
print({1, 2}.issubset(set1))  # True
print(set1.issuperset({1, 2}))  # True

# 字符串基础操作
# 字符串定义
# 单引号
s1 = 'Hello, World!'
# 双引号
s2 = "Hello, World!"
# 三引号（多行字符串）
s3 = """Hello,&#x20;
World!"""
# 原始字符串（不转义）
s4 = r'C:WindowsSystem32'  # 避免转义字符
print(s4)  # C:WindowsSystem32

# 字符串切片与索引
s = "Python is fun!"
print(s[0])      # P
print(s[1:4])    # yth
print(s[-1])     # !
print(s[::2])    # Pto isu
print(s[::-1])   # !nuf si nohtyP（反转）

# 字符串常用方法
s = "   Hello, Python!   "
# 去除空白
print(s.strip())    # "Hello, Python!"
print(s.lstrip())   # "Hello, Python!   "
print(s.rstrip())   # "   Hello, Python!"
# 大小写转换
print(s.upper())    # "   HELLO, PYTHON!   "
print(s.lower())    # "   hello, python!   "
print(s.title())    # "   Hello, Python!   "
# 查找子串
print(s.find("Python"))  # 7（找到）
print(s.find("Java"))    # -1（未找到）
print(s.index("Python")) # 7（找到）
# print(s.index("Java"))   # ValueError（未找到会报错）
# 替换子串
print(s.replace("Python", "World"))  # "   Hello, World!   "
# 分割字符串
print(s.split(", "))  # ['   Hello', 'Python!   ']
# 判断字符串类型
print(s.isalpha())    # False（包含空格和标点）
print(s.isdigit())    # False
print(s.startswith("   Hello"))  # True
print(s.endswith("!   "))        # True

# 字符串格式化
# 推荐使用 f-strings
name = "Alice"
age = 30
score = 95.5
# 基础用法
print(f"姓名：{name}，年龄：{age}岁")  # 姓名：Alice，年龄：30岁
# 表达式计算
print(f"明年年龄：{age + 1}岁")  # 明年年龄：31岁
# 格式化数字
print(f"成绩：{score:.1f}分")  # 成绩：95.5分
print(f"成绩：{score:.0f}分")  # 成绩：96分（四舍五入）
# 填充和对齐
print(f"姓名：{name:<10}")  # 左对齐，宽度10：姓名：Alice    &#x20;
print(f"成绩：{score:>10.1f}")  # 右对齐，宽度10：成绩：      95.5
# 数字格式化
number = 123456789
print(f"数字：{number:,}")  # 加千位分隔符：123,456,789
print(f"百分比：{0.75:.1%}")  # 百分比：75.0%
