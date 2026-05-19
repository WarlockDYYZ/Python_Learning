import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# 设置全局字体为“微软雅黑”（Windows系统自带）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# 解决负号显示成方块的问题
plt.rcParams['axes.unicode_minus'] = False
# 加载数据集
tips = sns.load_dataset("tips")


# 条形图（默认显示均值）
plt.figure()
sns.barplot(data=tips, x="day", y="total_bill", hue="smoker")

# 计数图（统计类别数量）
plt.figure()
sns.countplot(data=tips, x="day", hue="smoker")

# 显示其他统计量（如中位数）
plt.figure()
sns.barplot(
   data=tips,
   x="day", y="total_bill",
   estimator=np.median
)

plt.show()


# 点图与箱线图
# 点图（显示均值和置信区间）
sns.pointplot(data=tips, x="day", y="total_bill", hue="smoker",capsize=0.2)
# 箱线图
# sns.boxplot(data=tips, x="day", y="total_bill", hue="smoker")
plt.show()