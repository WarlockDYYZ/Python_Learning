import seaborn as sns
import matplotlib.pyplot as plt


# 设置全局字体为“微软雅黑”（Windows系统自带）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# 解决负号显示成方块的问题
plt.rcParams['axes.unicode_minus'] = False


tips = sns.load_dataset("tips")
iris = sns.load_dataset("iris")

# ========== 1. 2*2 普通轴级子图布局 ==========
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 左上 回归图
sns.regplot(data=tips, x="total_bill", y="tip", ax=axes[0,0])
axes[0,0].set_title("线性回归")

# 右上 箱线图
sns.boxplot(data=tips, x="day", y="total_bill", ax=axes[0,1])
axes[0,1].set_title("每日消费分布")

# 左下 直方图
sns.histplot(data=tips, x="tip", ax=axes[1,0], kde=True)
axes[1,0].set_title("小费分布")

# 右下 自定义折线
axes[1,1].plot([1,2,3,4],[2,4,1,3],"ro-")
axes[1,1].set_title("自定义图表")

plt.tight_layout()
plt.show()

# ========== 2. 独立弹窗：FacetGrid 分面图 ==========
g1 = sns.FacetGrid(tips, col="time", height=4)
g1.map(sns.histplot, "total_bill")
g1.fig.suptitle("按用餐时间分面直方图", y=1.02)
plt.show()

# ========== 3. 独立弹窗：PairGrid 成对关系图 ==========
g2 = sns.PairGrid(iris, hue="species", height=1.5)
g2.map(sns.scatterplot)
g2.add_legend()
plt.show()

# ========== 4. 独立弹窗：JointGrid 联合分布图 ==========
g3 = sns.JointGrid(data=tips, x="total_bill", y="tip", height=5)
g3.plot_joint(sns.regplot, color="orange")
g3.plot_marginals(sns.kdeplot, fill=True)
plt.show()