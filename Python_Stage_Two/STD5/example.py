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
