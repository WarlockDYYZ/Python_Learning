import pandas as pd
import numpy as np

# 1. 定义数据量和可选的分类值
n_rows = 20  # 这里我们生成20条测试数据
quarters = ['Q1', 'Q2', 'Q3', 'Q4']
categories = ['电子产品', '家居用品', '服装配饰', '食品饮料']

# 2. 构建 DataFrame
df = pd.DataFrame({
    '季度': np.random.choice(quarters, n_rows),       # 从四个季度中随机抽取
    '产品类别': np.random.choice(categories, n_rows),   # 从四个类别中随机抽取
    '价格': np.random.randint(50, 1000, n_rows),      # 随机生成 50-999 之间的整数作为价格
    '销量': np.random.randint(10, 500, n_rows)        # 随机生成 10-499 之间的整数作为销量
})

quarterly_mean = df.groupby('季度')['价格'].mean()
print(quarterly_mean)
print()

# 不在同一行
quarterly_mean = df.groupby('季度')[['价格', '销量']].mean()
print(quarterly_mean)
print()

# 在同一行
df_grouped = df.groupby(['季度', '产品类别'])['销量'].mean()
print(df_grouped)
print()
print(df.groupby(['季度', '产品类别']).mean())
print()


# 聚合函数使用示例
df = pd.DataFrame({
    "班级": ["1班", "1班", "2班", "2班"],
    "姓名": ["小明", "小刚", "小李", "小丽"],
    "数学": [85, 78, 88, 90],
    "语文": [92, 80, 85, 82]
})

# 按“班级”分组，并对“数学”求平均值，对“语文”求最大值
result = df.groupby("班级").agg({
    "数学": "mean",
    "语文": "max"
})
print(result)
print(result.index.name)
print(result.loc["1班"])
# 输出示例
#         价格               销量
#         mean       std     sum   count
# 季度
# Q1      500.0    141.42   1000      2
# Q2      600.0    100.00   1800      3
