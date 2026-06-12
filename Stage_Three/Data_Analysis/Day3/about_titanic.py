import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 加载官方经典数据集
df = sns.load_dataset('titanic')

# 基础统计分析
print(df.describe(include='all'))  # 输出全字段统计摘要
print("年龄中位数：", df['age'].median())  # 用中位数反映乘客年龄集中水平
print("票价偏度：", df['fare'].skew())  # 验证票价分布右偏特征
print("票价峰度：", df['fare'].kurt())  # 验证票价极端值分布特征

# 可视化分布特征
plt.figure(figsize=(18, 5))

# 年龄分布直方图+核密度曲线
plt.subplot(1, 3, 1)
sns.histplot(df['age'], kde=True, bins=20)
plt.title('乘客年龄分布')

# 舱位-票价箱线图
plt.subplot(1, 3, 2)
sns.boxplot(x='class', y='fare', data=df)
plt.title('不同舱位的票价分布')

# 数值相关性热力图 (新增部分)
plt.subplot(1, 3, 3)
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('数值特征相关性热力图')

plt.tight_layout()
plt.show()