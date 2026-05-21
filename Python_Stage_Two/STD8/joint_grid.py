import seaborn as sns
import matplotlib.pyplot as plt


# 设置全局字体为“微软雅黑”（Windows系统自带）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# 解决负号显示成方块的问题
plt.rcParams['axes.unicode_minus'] = False


# 加载数据集
tips = sns.load_dataset("tips")


# 基础使用
# 创建联合网格
g = sns.JointGrid(data=tips, x="total_bill", y="tip")
# 主图：散点图
g.plot_joint(sns.scatterplot)
# 边际图：直方图
g.plot_marginals(sns.histplot, bins=20, color="g", alpha=0.7)


g = sns.JointGrid(data=tips, x="total_bill", y="tip")
# 主图：回归分析
g.plot_joint(sns.regplot, color="#2E86AB")
# 边际图：密度图
g.plot_marginals(sns.kdeplot, fill=True, color="#A23B72")

plt.show()


# 高级应用
# 六边形分箱图
g = sns.JointGrid(data=tips, x="total_bill", y="tip")
g.plot_joint(plt.hexbin, gridsize=20, cmap="Blues")
g.plot_marginals(sns.histplot, bins=20, color="black", alpha=0.3)


# 自定义颜色映射
def hexbin(x, y, color, **kwargs):
    cmap = sns.light_palette(color, as_cmap=True)
    plt.hexbin(x, y, gridsize=15, cmap=cmap, **kwargs)


g = sns.JointGrid(data=tips, x="total_bill", y="tip")
# 自定义 hexbin 函数，自动生成渐变配色
g.plot_joint(hexbin, color="red", alpha=0.5)
# 边际分布图也用红色填充，保持整体风格统一
g.plot_marginals(sns.kdeplot, color="red", fill=True)

plt.show()