import seaborn as sns
import matplotlib.pyplot as plt


# 设置全局字体为“微软雅黑”（Windows系统自带）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# 解决负号显示成方块的问题
plt.rcParams['axes.unicode_minus'] = False
# 加载数据集
tips = sns.load_dataset("tips")


# 创建基础FacetGrid
tips = sns.load_dataset("tips")
g = sns.FacetGrid(tips, col="time")
# 在网格上绘制图表（使用map方法）
g.map(sns.histplot, "tip")

# 更复杂的分面（行和列）
g = sns.FacetGrid(tips, row="smoker", col="time", margin_titles=True)
g.map(sns.scatterplot, "total_bill", "tip", alpha=0.7)
g.add_legend()

plt.show()