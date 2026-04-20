import csv
import os
import datetime

# 文件操作与异常处理

# 6.1 文件读写操作
# 复习要点
# - 文件打开模式（r、w、a、r + 等）
# - with语句的使用
# - 文件读写方法（read、write、readline、readlines）
# - CSV 文件的读写操作

# 文件打开模式详解
# 常用文件打开模式
modes = {
    'r': '只读模式（默认），文件必须存在',
    'w': '只写模式（覆盖），文件不存在则创建，存在则清空',
    'a': '追加模式，文件不存在则创建，在末尾添加内容',
    'r+': '读写模式，文件必须存在',
    'w+': '读写模式（覆盖），文件不存在则创建，存在则清空',
    'a+': '读写追加模式，文件不存在则创建，写操作只能追加',
    'rb': '二进制只读模式',
    'wb': '二进制只写模式',
    'ab': '二进制追加模式'
}

for mode, desc in modes.items():
    print(f"{mode}: {desc}")
print("*" * 50)

# 基本文件操作流程
# 使用with语句安全打开文件
with open('example.txt', 'w', encoding='utf-8') as f:
    # 写入内容
    f.write("Hello, World!\n")
    f.write("这是一个示例文件。\n")
    f.write("第二行内容。\n")
# 使用with语句读取文件
with open('example.txt', 'r', encoding='utf-8') as f:
    # 读取全部内容
    content = f.read()
    print("文件内容：")
    print(content)
# 逐行读取大文件
with open('File/large_file', 'r', encoding='utf-8') as f:
    for line in f:
        print(line.strip())  # 去除换行符
print("*" * 50)

# CSV 文件操作
# 写入CSV文件
data = [
    ["姓名", "年龄", "城市"],
    ["张三", "25", "北京"],
    ["李四", "22", "上海"],
    ["王五", "30", "广州"]
]
# 'w'：写入模式
# newline=''：防止写入 CSV 多出空行（Windows 必须加）
# encoding='utf-8'：支持中文
# writer.writerows(data)：一次性写入所有行
with open('people.csv', 'w', newline='', encoding='utf-8') as f:
    # 把文件对象f包装成一个CSV写入工具，专门用来按CSV格式写数据
    # csv：Python自带的处理CSV文件的内置模块
    # csv.writer()：创建一个CSV 写入器对象
    # f：你打开的文件对象（open()得到的）
    # writer：你给这个写入工具起的名字（随便起名，一般叫writer）

    # 以后想往CSV文件里写行、写数据，不用自己拼逗号、换行，直接调用这个工具就行

    # writerow() —— 写一行
    # writerows() —— 写多行（代码里用的）
    # 不用 csv.writer f.write("姓名,年龄,城市\n")
    # 用了 writer.writerow(["姓名", "年龄", "城市"])
    # reader 类似
    writer = csv.writer(f)
    writer.writerows(data)
# 读取CSV文件
with open('people.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
# 使用DictReader读取CSV（带表头）
with open('people.csv', 'r', encoding='utf-8') as f:
    # DictReader把第一行当作键（key）
    # 可以直接用row['姓名']取值，不用记下标！
    reader = csv.DictReader(f)
    for row in reader:
        print(f"姓名：{row['姓名']}，年龄：{row['年龄']}，城市：{row['城市']}")
print("*" * 50)

# 练习 1：文本文件操作
# 1. 创建一个文件，写入10行内容（"第1行"、"第2行"...）
with open('lines.txt', 'w', encoding='utf-8') as f:
    for i in range(1, 11):
        f.write(f"这是第{i}行内容。\n")
# 2. 读取文件内容，打印行数和内容
with open('lines.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print(f"文件共有{len(lines)}行")
    for i, line in enumerate(lines, 1):
        print(f"第{i}行：{line.strip()}")
# 3. 统计文件中的字符数（不含换行符）
with open('lines.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    char_count = len(content.replace('\n', ''))
    print(f"文件字符数（不含换行符）：{char_count}")
# 4. 将文件内容反转（第一行变最后一行）
with open('lines.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
with open('reversed_lines.txt', 'w', encoding='utf-8') as f:
    # reversed(lines) 作用：把一个序列「倒序反转」，返回一个反向的迭代器
    # reversed()不会修改原列表
    # 它返回的是一个迭代器，不占额外内存
    # 只能遍历一次
    # 想直接得到反转列表：list(reversed(lines))
    for line in reversed(lines):
        f.write(line)
print("文件内容已反转并保存到reversed_lines.txt")
print("*" * 50)

# 练习 2：二进制文件操作
# 1. 复制图片文件（二进制操作）
with open('source.jpg', 'rb') as src, open('dest.jpg', 'wb') as dest:
    # 逐块读取和写入
    chunk_size = 4096
    while True:
        chunk = src.read(chunk_size)
        if not chunk:
            break
        dest.write(chunk)
print("图片文件已复制完成")
# 2. 统计二进制文件大小
file_size = os.path.getsize('source.jpg')
print(f"源文件大小：{file_size}字节")
print(f"目标文件大小：{os.path.getsize('dest.jpg')}字节")
# 3. 读取并显示图片文件的前10个字节（十六进制）
with open('source.jpg', 'rb') as f:
    header = f.read(10)
    print("文件前10个字节（十六进制）：")
    for byte in header:
        print(f"{byte:02X}", end=" ")
print()
print("*" * 50)

# 练习 3：CSV 文件高级操作
# 1. 从CSV文件读取数据，计算平均值
# 假设scores.csv包含学生成绩
# 姓名,语文,数学,英语
# 张三,85,90,88
# 李四,75,85,92
# 王五,90,87,95
with open('scores.csv', 'r', encoding='utf-8') as f:
    # reader = csv.DictReader(f)
    # 把CSV文件读成「字典」，每一行都是一个字典，用表头当键直接取值
    # 把第一行当作字典的key（键）
    # 后面每一行数据 → 变成一个字典

    # 姓名, 年龄, 城市
    # 张三, 25, 北京
    # 李四, 22, 上海
    # to
    # {"姓名": "张三", "年龄": "25", "城市": "北京"}
    # {"姓名": "李四", "年龄": "22", "城市": "上海"}

    reader = csv.DictReader(f)
    total_scores = []
    for row in reader:
        # 转换为整数
        scores = [int(row['语文']), int(row['数学']), int(row['英语'])]
        avg_score = sum(scores) / len(scores)
        total_scores.append(avg_score)
        print(f"{row['姓名']}的平均分：{avg_score:.1f}")

    if total_scores:
        overall_avg = sum(total_scores) / len(total_scores)
        print(f"全体学生平均分：{overall_avg:.1f}")
# 2. 写入一个包含时间戳的CSV文件
with open('log.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    # 写入表头（如果文件为空）
    if os.path.getsize('log.csv') == 0:
        writer.writerow(['时间', '操作', '结果'])
    # 写入日志记录
    # 这行代码的作用：获取当前系统时间，并格式化成: 年-月-日 时:分:秒
    # datetime Python处理日期时间的内置模块
    # datetime.datetime 从 datetime 模块里，找到 datetime类
    # .now()获取当前的系统时间
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    writer.writerow([timestamp, '文件操作练习', '成功'])
# 3. 使用csv模块读取复杂格式的CSV
# 假设文件内容：姓名|年龄|城市（分隔符为|）
with open('people.txt', 'r', encoding='utf-8') as f:
    # 读取使用 | 作为分隔符的文件（不是默认逗号）
    # delimiter就是指定「用什么符号来切分每一行的列」
    reader = csv.reader(f, delimiter='|')
    for row in reader:
        print(f"姓名：{row[0]}，年龄：{row[1]}，城市：{row[2]}")
print("*" * 50)

# 6.2 异常处理机制
# 复习要点
# - 异常处理的基本语法（try-except-else-finally）
# - 常见异常类型（FileNotFoundError、ZeroDivisionError、ValueError 等）
# - 自定义异常类
# - 异常的传递机制

# 异常处理基本语法
# 基本异常处理结构
try:
    # 可能抛出异常的代码
    x = 10 / 0
except ZeroDivisionError as e:
    # 处理除零异常
    print(f"发生除零错误：{e}")
except ValueError as e:
    # 处理值错误
    print(f"发生值错误：{e}")
except Exception as e:
    # 处理其他所有异常
    print(f"发生其他异常：{e}")
else:
    # 没有异常时执行
    print("代码执行成功")
finally:
    # 无论是否发生异常都会执行
    print("finally块执行")
print("*" * 50)

# 常见异常类型
# 常见异常类型及触发场景
exceptions = {
    'FileNotFoundError': '文件不存在',
    'ZeroDivisionError': '除以零',
    'ValueError': '值错误（如类型转换失败）',
    'TypeError': '类型错误（如字符串和数字相加）',
    'IndexError': '索引越界',
    'KeyError': '字典键不存在',
    'AttributeError': '对象没有该属性',
    'IOError': '输入输出错误',
    'MemoryError': '内存不足',
    'TimeoutError': '操作超时'
}
for exc_type, desc in exceptions.items():
    print(f"{exc_type}: {desc}")
print("*" * 50)


# 自定义异常
# 自定义异常类
class InvalidAgeError(Exception):
    """年龄无效异常"""

    def __init__(self, age, message="年龄必须在0-150之间"):
        self.age = age
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.age} 是无效的年龄。{self.message}"


# 使用自定义异常
try:
    # age = int(input("请输入年龄："))
    age = 10000
    if age < 0 or age > 150:
        raise InvalidAgeError(age)
    print(f"输入的年龄是：{age}")
except InvalidAgeError as e:
    print(f"自定义异常：{e}")
# 输入 199.9 → 得到字符串 "199.9" → 传给 int() 转换失败→ 触发 except ValueError
except ValueError:
    print("错误：请输入有效的整数年龄")
print("*" * 50)


# 练习 4：异常处理实战
# 1. 安全的文件读取函数
def safe_read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"错误：文件 {file_path} 不存在")
        return None
    except PermissionError:
        print(f"错误：没有权限读取文件 {file_path}")
        return None
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
        return None


# 测试
content = safe_read_file('example.txt')
if content:
    print("文件内容：")
    print(content)


# 2. 安全的除法函数
def safe_divide(a, b):
    try:
        if b == 0:
            raise ValueError("除数不能为0")
        return a / b
    except TypeError:
        print("错误：参数必须是数字")
        return None
    except ValueError as e:
        print(f"错误：{e}")
        return None


# 测试
print(safe_divide(10, 2))  # 输出：5.0
print(safe_divide(10, 0))  # 输出：错误：除数不能为0
print(safe_divide(10, '2'))  # 输出：错误：参数必须是数字
print()
print("*" * 50)


# 3. 安全的类型转换函数
def safe_convert_to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        print(f"无法将 {value} 转换为整数")
        return None


# 测试
print(safe_convert_to_int("123"))  # 输出：123
print(safe_convert_to_int("abc"))  # 输出：无法将 abc 转换为整数
# 与前面不同，该处的3.14为数字类型可以转换，上方"123",转换后为整数可以转换，"1.23"就无法转换
print(safe_convert_to_int(3.14))  # 输出：3
print(safe_convert_to_int(True))  # 输出：1
print("*" * 50)


# 练习 5：自定义异常应用
# 1. 创建一个工资计算异常
class SalaryCalculationError(Exception):
    """工资计算错误异常"""
    pass


class NegativeHoursError(SalaryCalculationError):
    """工时为负数异常"""

    def __init__(self, hours):
        super().__init__(f"工时 {hours} 不能为负数")


class NegativeRateError(SalaryCalculationError):
    """工资率为负数异常"""

    def __init__(self, rate):
        super().__init__(f"工资率 {rate} 不能为负数")


# 计算工资函数
def calculate_salary(hours, rate):
    if hours < 0:
        raise NegativeHoursError(hours)
    if rate < 0:
        raise NegativeRateError(rate)
    return hours * rate


# 测试工资计算
try:
    salary = calculate_salary(40, 25)
    print(f"工资：{salary}元")
    salary = calculate_salary(-5, 25)  # 工时为负
except SalaryCalculationError as e:
    print(f"工资计算错误：{e}")
print("." * 50)


# 2. 自定义一个数据库连接异常
class DatabaseConnectionError(Exception):
    """数据库连接错误"""

    def __init__(self, host, port, message="数据库连接失败"):
        self.host = host
        self.port = port
        self.message = message
        super().__init__(f"{message}：{host}:{port}")


# 模拟数据库连接
def connect_to_database(host, port, max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        try:
            print(f"尝试连接 {host}:{port} (第{attempt}次)")
            # 这里模拟连接失败
            if host == "localhost" and port == 3306:
                print("连接成功！")
                return True
            else:
                raise DatabaseConnectionError(host, port, "无效的主机或端口")
        except DatabaseConnectionError as e:
            if attempt < max_attempts:
                print(f"连接失败：{e}，重试中...")
            else:
                print(f"连接失败：{e}，已达到最大重试次数")
                return False


# 测试数据库连接
connect_to_database("localhost", 3306)  # 成功连接
connect_to_database("wrong_host", 8080)  # 失败
print("*" * 50)


# 练习 6：异常传递机制
# 1. 异常在函数调用栈中的传递
def func1():
    func2()


def func2():
    func3()


def func3():
    x = 10 / 0  # 这里会抛出异常


try:
    func1()
except ZeroDivisionError as e:
    print(f"在最外层捕获到异常：{e}")
# func1() -> func2() -> func3(), 执行func1()时， func3()出现异常没有定义异常处理，抛给func2(), func2()中同样没有异常处理
# 抛给func1(), 在func1()执行处有异常处理
print("." * 50)


# 2. 异常处理的层次结构
def divide(a, b):
    return a / b


def calculate():
    try:
        result = divide(10, 0)
        print(f"计算结果：{result}")
    except ZeroDivisionError:
        print("在calculate()中捕获到除零错误")
        raise  # 重新抛出异常


try:
    calculate()
except ZeroDivisionError:
    print("在主程序中再次捕获到除零错误")
# 第一步：执行 divide(10, 0)
# 调用 divide 函数，计算 10 / 0
# 触发 ZeroDivisionError 除零异常
# divide 函数没有处理异常，异常向上抛给调用它的 calculate
# 第二步：calculate 捕获异常
# calculate 里的 try-except 捕获到了异常
# 打印：在calculate()中捕获到除零错误
# 执行 raise：把这个异常再次抛出去（不自己消化，继续向上传）
# 第三步：异常传到主程序的 try-except
# calculate() 抛出的异常被主程序的 except ZeroDivisionError 捕获
# 第四步：主程序打印最终信息
# 打印：在主程序中再次捕获到除零错误
# 程序正常结束，不会崩溃
print("." * 50)


# 3. 模拟一个复杂的异常处理场景
def read_config(param):
    """读取配置文件"""
    # 模拟：文件不存在，直接抛出异常
    raise FileNotFoundError()
    pass


def validate_config(config):
    """验证配置文件"""
    pass


def perform_operation(config):
    """执行操作"""
    pass


def complex_operation():
    try:
        config = read_config('config.txt')
        validate_config(config)
        result = perform_operation(config)
        return result
    except FileNotFoundError:
        print("错误：配置文件不存在")
        raise  # 重新抛出，让调用者处理
    except ValueError as e:
        print(f"错误：配置文件格式错误 - {e}")
    except Exception as e:
        print(f"执行操作时发生意外错误：{e}")
    finally:
        print("清理资源...")


# 调用复杂操作
try:
    complex_operation()
# complex_operation 重新抛出的异常
except FileNotFoundError:
    print("警告：使用默认配置")
print("*" * 50)


# 6.3 文件操作与异常处理综合练习
# 复习要点
# - 文件操作中的异常处理
# - 批量文件处理
# - 数据备份与恢复

# 文件操作异常处理示例
# 安全的文件复制函数
def safe_copy_file(src_path, dest_path):  # 源路径，目标路径
    try:
        # 检查源文件是否存在
        if not os.path.exists(src_path):
            raise FileNotFoundError(f"源文件 {src_path} 不存在")

        # 检查是否有权限读取
        if not os.access(src_path, os.R_OK):
            raise PermissionError(f"没有权限读取 {src_path}")

        # 检查目标目录是否存在
        dest_dir = os.path.dirname(dest_path)
        if dest_dir and not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        # 分块复制文件(大文件也不会卡死), 用 with 自动关闭文件
        with open(src_path, 'rb') as src, open(dest_path, 'wb') as dest:
            while True:
                chunk = src.read(4096)
                if not chunk:
                    break
                dest.write(chunk)

        print(f"文件已成功复制：{src_path} → {dest_path}")

    except Exception as e:
        print(f"文件复制失败：{e}")
        # 如果目标文件已创建，删除它
        if os.path.exists(dest_path):
            try:
                os.remove(dest_path)
                print(f"已删除不完整的目标文件：{dest_path}")
            except Exception as e2:
                print(f"删除不完整文件时发生错误：{e2}")
        raise  # 重新抛出异常


# 正常调用
try:
    safe_copy_file("test.txt", "copy/test_copy.txt")
except Exception as e:
    print(f"最终处理：{e}")
print("*" * 50)


# 练习 7：批量文件处理
# 1. 批量重命名文件（添加前缀）
def batch_rename_files(directory, prefix):
    """批量重命名目录下的所有文件，添加指定前缀"""
    try:
        # os.path.isdir(path)
        # 作用：判断一个路径是不是文件夹（目录）
        # 返回：True / False
        # 中文意思： is directory？是目录吗？
        if not os.path.isdir(directory):
            raise NotADirectoryError(f"{directory} 不是一个目录")

        # 全称：list directory → 列出目录里的内容
        # 作用：拿到一个文件夹里所有文件和子文件夹的名字
        for filename in os.listdir(directory):
            print(filename)
            old_path = os.path.join(directory, filename)

            # 跳过目录
            if os.path.isdir(old_path):
                continue

            # 构建新文件名
            new_filename = f"{prefix}_{filename}"
            new_path = os.path.join(directory, new_filename)

            # 重命名文件
            os.rename(old_path, new_path)
            print(f"重命名：{old_path} → {new_path}")

    except Exception as e:
        print(f"批量重命名失败：{e}")


# 测试, 运行过来，成功，因为后面要测试其他代码，为防止反复修改文件名，注释调用
# batch_rename_files(r'D:\pythonProject\Python\Rename_File', '照片')
print("." * 50)


# 2. 批量复制文件到指定目录
def batch_copy_files(src_dir, dest_dir, file_extensions=None):
    """
   批量复制文件到目标目录
   file_extensions: 可选，指定文件扩展名列表（如['.txt', '.csv']）
   """
    try:
        if not os.path.isdir(src_dir):
            raise NotADirectoryError(f"源目录 {src_dir} 不存在")

        # 目标目录不存在责创建目录
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        for filename in os.listdir(src_dir):
            src_path = os.path.join(src_dir, filename)

            # 检查是否为文件
            if not os.path.isfile(src_path):
                continue

            # 检查文件扩展名（如果指定）
            if file_extensions:
                ext = os.path.splitext(filename)[1].lower()
                if ext not in file_extensions:
                    continue

            # 复制文件
            dest_path = os.path.join(dest_dir, filename)
            safe_copy_file(src_path, dest_path)

    except Exception as e:
        print(f"批量复制失败：{e}")


# 测试：复制所有txt和csv文件
# 本级文件夹，不用加那些前缀如 C://...
batch_copy_files('source_dir', 'dest_dir', ['.txt', '.csv'])
print("." * 50)


# 3. 清理临时文件
def clean_temp_files(temp_dir, max_days=7):
    """
   清理临时目录中的旧文件
   max_days: 保留文件的最大天数
   """
    import time

    try:
        if not os.path.isdir(temp_dir):
            raise NotADirectoryError(f"临时目录 {temp_dir} 不存在")

        current_time = time.time()
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)

            # 只处理文件
            if not os.path.isfile(file_path):
                continue

            # 获取文件修改时间
            # os.path.getmtime(文件路径) = 获取这个文件最后一次被修改的时间
            # 返回一个数字，叫时间戳（timestamp）单位：秒表示：从1970年1月1日到文件最后修改时间的总秒数
            mtime = os.path.getmtime(file_path)

            # 计算文件年龄（天）
            age_days = (current_time - mtime) / (24 * 3600)

            # 如果文件超过指定天数，删除
            if age_days > max_days:
                try:
                    os.remove(file_path)
                    print(f"已删除旧文件：{file_path}（年龄：{age_days:.1f}天）")
                except Exception as e:
                    print(f"删除文件 {file_path} 失败：{e}")

    except Exception as e:
        print(f"清理临时文件失败：{e}")


# 测试
clean_temp_files('dest_dir', 7)
print("*" * 50)


# 练习 8：数据备份系统
# 简单的数据备份系统
def create_backup(source, destination, backup_name=None):
    """创建数据备份"""
    import shutil

    try:
        # 如果未指定备份名称，使用时间戳
        if not backup_name:
            import datetime
            backup_name = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

        # 创建备份目录
        backup_dir = os.path.join(destination, backup_name)
        os.makedirs(backup_dir)

        # 复制文件
        if os.path.isfile(source):
            # 单个文件备份
            shutil.copy2(source, backup_dir)
            print(f"已备份文件：{source} → {backup_dir}")
        elif os.path.isdir(source):
            # 目录备份
            shutil.copytree(source, os.path.join(backup_dir, os.path.basename(source)))
            print(f"已备份目录：{source} → {backup_dir}")
        else:
            raise FileNotFoundError(f"源路径 {source} 不存在")

        return backup_dir

    except Exception as e:
        print(f"备份失败：{e}")
        # 清理已创建的不完整备份
        if os.path.exists(backup_dir):
            try:
                shutil.rmtree(backup_dir)
                print(f"已删除不完整的备份目录：{backup_dir}")
            except Exception as e2:
                print(f"清理不完整备份失败：{e2}")
        raise


# 恢复备份
def restore_backup(backup_path, destination):
    """恢复数据备份"""
    import shutil

    try:
        # 获取备份内容
        backup_contents = os.listdir(backup_path)

        if len(backup_contents) == 1:
            # 备份是单个文件或目录
            source_item = os.path.join(backup_path, backup_contents[0])
            if os.path.isfile(source_item):
                # 恢复单个文件
                shutil.copy2(source_item, destination)
                print(f"已恢复文件：{source_item} → {destination}")
            else:
                # 恢复目录
                shutil.copytree(source_item, destination, dirs_exist_ok=True)
                print(f"已恢复目录：{source_item} → {destination}")
        else:
            # 备份包含多个文件，直接复制所有内容
            for item in backup_contents:
                source_item = os.path.join(backup_path, item)
                dest_item = os.path.join(destination, item)
                if os.path.isfile(source_item):
                    shutil.copy2(source_item, dest_item)
                    print(f"已恢复文件：{source_item} → {dest_item}")
                else:
                    shutil.copytree(source_item, dest_item, dirs_exist_ok=True)
                    print(f"已恢复目录：{source_item} → {dest_item}")

    except Exception as e:
        print(f"恢复失败：{e}")
        raise


# 测试备份系统
# 1. 创建
# 备份
create_backup("my_folder", "my_backups")
# 恢复（把刚才的备份路径填进去）
restore_backup("my_backups/20260420_234301", "restore_folder")
