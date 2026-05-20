import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


# 设置全局字体为“微软雅黑”（Windows系统自带）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# 解决负号显示成方块的问题
plt.rcParams['axes.unicode_minus'] = False


# 加载鸢尾花数据集
iris = sns.load_dataset("iris")
# 加载数据集
tips = sns.load_dataset("tips")
# print(iris)


# 使用基础
# 创建基础 PairGrid
g = sns.PairGrid(iris)
g.map_diag(sns.histplot)  # 对角线：直方图
g.map_offdiag(sns.scatterplot)  # 非对角线：散点图

# 按类别着色
g = sns.PairGrid(iris, hue="species")
g.map_diag(sns.kdeplot)
g.map_offdiag(sns.scatterplot)
g.add_legend()
plt.show()


# 高级配置
# 选择特定变量
# 加上 corner=True 会导致一些坐标轴标签的显示问题，虽然可解决，但带来的不适与获得的便利，我认为不成正比，所以此处仅了解，实际应用中知道可以解决即可
# g = sns.PairGrid(iris, vars=["sepal_length", "sepal_width"], hue="species", corner=True)
g = sns.PairGrid(iris, vars=["sepal_length", "sepal_width"], hue="species")

# 单独设置对角线：绘制直方图 (或者用 sns.kdeplot 画密度曲线)
g.map_diag(sns.histplot)

# 单独设置非对角线：绘制散点图
# g.map_offdiag(sns.scatterplot)
g.map_offdiag(sns.kdeplot, fill=True)
# 填充的密度图(和上面的内容二选一)
# g.map_lower(sns.kdeplot, fill=True)

# 加图例
g.add_legend()

# 上下三角使用不同函数
g = sns.PairGrid(iris)
g.map_upper(sns.scatterplot)
g.map_lower(sns.kdeplot, fill=True)
g.map_diag(sns.histplot)

# 单列/单行配置
g = sns.PairGrid(tips, y_vars=["tip"], x_vars=["total_bill", "size"], height=4)
g.map(sns.scatterplot)

plt.show()


# 使用pairplot快捷创建
sns.pairplot(iris, hue="species", height=2.5)

# 更多配置选项
sns.pairplot(
    iris,
    hue="species",
    palette="Set2",
    diag_kind="kde",
    height=2.5
)
plt.show()
