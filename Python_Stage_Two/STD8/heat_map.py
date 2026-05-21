import seaborn as sns
import matplotlib.pyplot as plt


# 设置全局字体为“微软雅黑”（Windows系统自带）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# 解决负号显示成方块的问题
plt.rcParams['axes.unicode_minus'] = False
# 加载数据集(鸢尾花)
iris = sns.load_dataset("iris")
tips = sns.load_dataset("tips")


# 创建相关系数矩阵
iris_corr = iris.corr(numeric_only=True)
print(iris_corr)

# 基础热力图
# sns.heatmap(iris_corr, annot=True, cmap="RdBu")

# 自定义配置
sns.heatmap(
    iris_corr,
    annot=True,          # 显示数值
    fmt=".2f",          # 数值格式
    cmap="YlGnBu",      # 颜色映射
    linewidths=0.5,      # 单元格边框宽度
    linecolor="black",   # 边框颜色
    square=True          # 单元格为正方形
)
plt.title("鸢尾花特征相关性热力图") # 加个标题

plt.show()


# 带层次聚类的热力图
# 数据重塑（从长表到宽表）
flights = sns.load_dataset("flights")
flights_wide = flights.pivot(index="year", columns="month", values="passengers")

# 聚类热力图
g = sns.clustermap(
    flights_wide,
    cmap="YlGnBu",
    row_cluster=True,    # 行聚类
    col_cluster=True,    # 列聚类
    figsize=(6, 6),      # 设置图形尺寸
    # 在 clustermap（聚类热力图）中，square=True 参数会被直接忽略
    # square=True
    cbar=True,  # 默认为 True，设为 False 就会隐藏图例
    cbar_kws={"label": "乘客数量", "shrink": 0.8}  # 给图例加个标题，并稍微缩小一点尺寸
)
plt.show()

# 自定义聚类配置
g = sns.clustermap(
    flights_wide,
    method="ward",       # 聚类方法
    metric="euclidean",  # 距离度量
    cmap="magma",        # 岩浆 深黑紫色（代表最小值） -> 亮橙色 -> 明亮的黄色（代表最大值）
    row_cluster=False,    # 行聚类
    col_cluster=False,    # 列聚类
    figsize=(6, 6)
)
plt.show()
