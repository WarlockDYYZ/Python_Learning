# 列表
# 1. 创建一个包含1到10的列表
numbers = [x+1 for x in range(10)]
print(numbers)
# 2. 删除偶数
# 方法1：使用列表推导式
numbers_1 = [x + 1 for x in range(10) if x % 2 == 1]
print(numbers_1)
# 方法2：使用循环和remove()（注意陷阱）
# 注意：直接循环删除会跳过元素，需要从后往前删
for i in range(len(numbers)-1, -1, -1):
    if numbers[i] % 2 == 1:
        numbers.remove(numbers[i])
print(numbers)
# 3. 添加数字11到20（注意：是添加到列表末尾）
# 方法1：使用extend()
numbers_1.extend([x + 11 for x in range(10)])
print(numbers_1)
# # 方法2：使用列表推导式和加法
numbers += [x + 11 for x in range(10)]
print(numbers)
# 4. 反转列表
numbers.reverse()
print(f"反转后：{numbers}")
# 5. 排序（降序）
numbers.reverse()
print(f'原列表：{numbers}')
numbers.sort(reverse=True)
print(f"降序排序后：{numbers}")
# 6. 找出最大值和最小值
max_num = max(numbers)
min_num = min(numbers)
print(f"最大值：{max_num}，最小值：{min_num}")
# 7. 计算平均值
avg = sum(numbers) / len(numbers)
print(f"平均值：{avg:.2f}")

# 字典
# 1. 创建一个学生信息字典
student = {
   "name": "张三",
   "age": 20,
   "courses": {
       "数学": 90,
       "语文": 85,
       "英语": 95
   }
}
# 2. 输出学生基本信息
print("学生信息：")
print(f"姓名：{student['name']}")
print(f"年龄：{student['age']}岁")
# 3. 计算平均成绩
courses = student["courses"]
total_score = sum(courses.values())
avg_score = total_score / len(courses)
print(f"平均成绩：{avg_score:.1f}分")
# 4. 找出最高分和最低分
max_score = max(courses.values())
min_score = min(courses.values())
print(f"最高分：{max_score}分")
print(f"最低分：{min_score}分")
# 5. 找出最高分的科目
# 方法1：遍历字典
max_subject = ""
for subject, score in courses.items():
   if score == max_score:
       max_subject = subject
       break
# 方法2：使用列表推导式
max_subjects = [subject for subject, score in courses.items() if score == max_score]
print(f"最高分科目：{max_subject}（{max_score}分）")
# 6. 添加一门新科目（物理，88分）
student["courses"]["物理"] = 88
print(f"添加物理后：{student['courses']}")
# 7. 删除语文科目
del student["courses"]["语文"]
print(f"删除语文后：{student['courses']}")
# 8. 输出所有科目和成绩（格式化）
print("n所有科目成绩：")
for subject, score in courses.items():
   print(f"{subject}：{score}分")
# 字符串处理练习
# 1. 定义一个字符串
s = "   Hello, Python World!   "
# 2. 去除首尾空格
s_stripped = s.strip()
print(f"去除空格后：{s_stripped}")
# 3. 转换为大写
s_upper = s_stripped.upper()
print(f"大写：{s_upper}")
# 4. 转换为小写
s_lower = s_stripped.lower()
print(f"小写：{s_lower}")
# 5. 统计字符数（不包含空格）
s_without_space = s_stripped.replace(" ", "")
print(f"字符数（不含空格）：{len(s_without_space)}")
# 6. 统计单词数
words = s_stripped.split()
print(f"单词数：{len(words)}")
# 7. 找出"Python"的位置
python_index = s_stripped.find("Python")
print(f"'Python'出现在索引：{python_index}")
# 8. 替换"Python"为"Java"
s_replaced = s_stripped.replace("Python", "Java")
print(f"替换后：{s_replaced}")
# 9. 反转字符串
s_reversed = s_stripped[::-1]
print(f"反转后：{s_reversed}")
# 10. 格式化输出
print("n格式化输出：")
print(f"原始字符串：{s}")
print(f"处理后字符串：{s_stripped}")
print(f"长度：{len(s_stripped)}")
print(f"首字母：{s_stripped[0]}")
print(f"尾字母：{s_stripped[-1]}")