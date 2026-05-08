import re


def print_star():
    print(100 * "*")


# 预编译手机号正则表达式
# 1开头，第二个字符是 3到9 任意，任意数字匹配 9 次
phone_pattern = re.compile(r"^1[3-9]\d{9}$")

# 多次使用预编译的正则
phone1 = "13812345678"
phone2 = "12345678901"
print(phone_pattern.match(phone1))  # 匹配成功，返回Match对象
print(phone_pattern.match(phone2))  # 匹配失败，返回None
print_star()

print(re.findall(r'[a-z]', 'A1b2C3', re.I))
# ['A','b','C']

s = """hello
world
python
Test"""
# 匹配每行以小写字母开头
print(re.findall(r'^[a-z]+', s, re.M))
# ['hello', 'world', 'python']

s = "<div>内容\n换行</div>"
# .*?，任意字符，0个或多个，非贪婪匹配
res = re.findall(r'<div>.*?</div>', s)
print(res)
res = re.findall(r'<div>.*?</div>', s, re.S)
print(res)
# ['<div>内容\n换行</div>']

pat = r"""
^1        # 手机号以1开头
[3-9]     # 第二位3-9
\d{9}     # 后面9位数字
"""
res = re.match(pat, "13812345678", re.X)
print(res)
print_star()

# 2.1
html_text = """
<div class="content">
    <h1>Python正则表达式实战</h1>
    <p>在数据驱动的时代，原始数据中充斥着大量"噪音"——无关字符、不规则格式、隐藏的异常值。</p>
</div>
"""

# 去除所有HTML标签
# <[^>]+> 匹配 <  不是>的字符 （1个以上）  >
# 原文本中第一行前有一个换行符，所以结果有两个空行
clean_text = re.sub(r"<[^>]+>", "", html_text)
print("清洗后的文本：")
print(clean_text)

punctuation_text = "Hello, world! This is a test string. 123-456-7890"
# 去除所有标点符号
# 不匹配数字字母和下划线
clean_text = re.sub(r"[^\w\s]", "", punctuation_text)
print("去除标点后的文本：")
print(clean_text)  # 输出：Hello world This is a test string 1234567890

special_text = "user@example.com! Password: P@ssw0rd$"
# 去除指定的特殊符号
# [] 内任意一个字符
clean_text = re.sub(r"[!@#$%^&*()]", "", special_text)
print("去除特殊符号后的文本：")
print(clean_text)  # 输出：userexample.com Password: Pssw0rd
print_star()

# 提取整数
number_text = "Total: 123 items, Price: $45.99, Count: 7"
# 数字 一次或多次
integers = re.findall(r"\d+", number_text)
print("提取的整数：", integers)  # 输出：['123', '45', '99', '7']

# 提取小数（保留两位）
# 数字 1 次或 n 次  .  数字 恰好 2 次
decimals = re.findall(r"\d+.\d{2}", number_text)
print("提取的小数：", decimals)  # 输出：['45.99']

# 提取手机号（中国大陆）
phone_text = "联系电话：13812345678，备用号码：15987654321"
# 1 开头 数字 3~9 为第二个字符  后面9个数字
phones = re.findall(r"1[3-9]\d{9}", phone_text)
print("提取的手机号：", phones)  # 输出：['13812345678', '15987654321']

# 提取日期（YYYY-MM-DD格式）
date_text = "订单日期：2024-05-20，有效期：2024-12-31"
# 四个数字 - 两个数字 - 两个数字
dates = re.findall(r"\d{4}-\d{2}-\d{2}", date_text)
print("提取的日期：", dates)  # 输出：['2024-05-20', '2024-12-31']
print_star()

email_text = """
用户邮箱：user1@example.com
备用邮箱：user2.name@domain.org
工作邮箱：first.last@company.co.uk
"""
# 简化版邮箱匹配模式
email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+"
emails = re.findall(email_pattern, email_text)
print("提取的邮箱地址：")
for email in emails:
    print(f"- {email}")
print_star()

url_text = """
网站链接：https://www.example.com
文档地址：http://docs.example.org/document.pdf
图片链接：https://cdn.example.net/images/photo.jpg
"""
# URL匹配模式（简化版）
# 固定匹配http 0~1个s 固定匹配:// 不匹配空字符及特殊分割符 匹配一个 “不是空格、不是 / $.? #” 的正常字符 匹配任意一个字符 不匹配空字符 0~n
# [^\s/$.?#].[^\s]* ：第一个字符非空字符且非特殊字符，“.”第二个字符可以是任意内容，0~n 个非空字符
url_pattern = r"https?://[^\s/$.?#].[^\s]*"
urls = re.findall(url_pattern, url_text)
print("提取的URL地址：")
for url in urls:
    print(f"- {url}")
print_star()

date_text = "订单日期：05/20/2024，有效期：12/31/2024"
# 使用分组捕获和反向引用进行格式转换
converted_date = re.sub(r"(\d{2})/(\d{2})/(\d{4})", r"\3-\1-\2", date_text)
print("转换后的日期格式：")
print(converted_date)  # 输出：订单日期：2024-05-20，有效期：2024-12-31
print_star()


mixed_case_text = "Hello WORLD! This is a MiXeD CaSe TeSt."
# 转换为小写
lowercase_text = mixed_case_text.lower()
print("转换为小写：", lowercase_text)
# 转换为大写
uppercase_text = mixed_case_text.upper()
print("转换为大写：", uppercase_text)
print_star()


messy_whitespace = "  Hello   world!   This is   a   test.   "

# 去除首尾空白
stripped_text = messy_whitespace.strip()
print("去除首尾空白：", stripped_text)

# 合并连续空白为单个空格
clean_text = re.sub(r"\s+", " ", stripped_text)
print("合并连续空白：", clean_text)

# 标准化换行符（将\r\n转换为\n）
line_ending_text = "Line 1\r\nLine 2\nLine 3\rLine 4"
print("原字符串：", repr(line_ending_text))
normalized_text = re.sub(r"\r\n", "\n", line_ending_text)
print("标准化换行符：", repr(normalized_text))
# 因为都是换行符，所以正常输出两个结果是一样的
# repr() 函数将对象转化为供解释器读取的形式，就可以看见换行符的修改情况
print_star()


mixed_delimiter_text = "item1, item2; item3   item4;item5, item6"
# 使用正则表达式按多种分隔符分割
items = re.split(r'[;,\s]+', mixed_delimiter_text)
print("分割后的列表：", items)  # 输出：['item1', 'item2', 'item3', 'item4', 'item5', 'item6']
