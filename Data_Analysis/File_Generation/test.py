import pandas as pd
import random
import string

# 基础数据源
name_list = ["张三", "李四", "王五", "赵六", "孙丽", "周明", "吴杰", "郑浩", "马宁", "刘芳",
             "陈雪", "林强", "黄伟", "高敏", "徐婷"]
department_list = ["销售部", "市场部", "运营部", "技术部", "人事部", "财务部"]
product_category_list = ["数码", "家电", "服饰", "食品", "美妆", "家居"]
region_list = ["华北", "华东", "华南", "西南", "华中", "东北"]

# 混合日期（适配你之前的清洗练习）
date_clean = ["1978/3/27", "2015/8/30", "2016/5/12", "2017/11/5", "2018/2/18"]
date_time = ["2015/8/30 19:16", "2016/5/12 08:45", "2017/11/5 14:22"]
dirty_date = ["invalid", "", "2019/7", "null"]


# 生成随机邮箱（含脏数据）
def random_email():
    suffix = ["@qq.com", "@163.com", "@sina.com", "@gmail.com"]
    name_str = ''.join(random.sample(string.ascii_lowercase, random.randint(5, 10)))
    if random.random() < 0.1:
        return "invalid_email"
    return name_str + random.choice(suffix)


data = []
row_count = 500

for _ in range(row_count):
    name = random.choice(name_list)
    department = random.choice(department_list)
    product_category = random.choice(product_category_list)
    salary = random.randint(4000, 30000)
    sales = round(random.uniform(100.0, 9999.0), 2)
    region = random.choice(region_list)

    # 混合日期
    date_type = random.choices([date_clean, date_time, dirty_date], weights=[0.7, 0.2, 0.1])[0]
    date_val = random.choice(date_type)

    income = round(random.uniform(6000, 80000), 2)
    score = round(random.uniform(-3, 108), 2)  # 异常分数
    email = random_email()
    value = random.randint(10, 500)

    row = [name, department, product_category, salary, sales, region, date_val, income, score, email, value]
    data.append(row)

# 完整字段
columns = [
    "name",
    "department",
    "product_category",
    "salary",
    "sales",
    "region",
    "date",
    "income",
    "score",
    "email",
    "value"
]

df = pd.DataFrame(data, columns=columns)

# 保存文件
df.to_csv("data_clean_demo.csv", index=False, encoding="utf-8-sig")
print("✅ 数据生成成功！文件：data_clean_demo.csv")
print("\n📋 字段列表：")
print(columns)
print("\n📌 前5行数据：")
print(df.head())