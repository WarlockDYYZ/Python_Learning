import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


# 设置全局字体为“微软雅黑”（Windows系统自带）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# 解决负号显示成方块的问题
plt.rcParams['axes.unicode_minus'] = False


# 加载数据集
tips = sns.load_dataset("tips")


# 1. 改造自定义绘图函数
# 在新版中，建议让自定义函数直接接收 DataFrame (data) 以及 x, y 的列名 (字符串)
def qqplot(data, x, y, **kwargs):
    # 通过列名从当前子图的数据切片中提取实际的数值序列
    x_vals = data[x]
    y_vals = data[y]

    # 计算分位数
    # 返回(理论分位数, 样本分位数)，只需要样本分位数，理论分位数用 _ 丢弃
    _, xr = stats.probplot(x_vals, fit=False)
    _, yr = stats.probplot(y_vals, fit=False)

    # 绘制散点图
    plt.scatter(xr, yr, **kwargs)

    # ===================== 新增：趋势线 =====================
    # 两条趋势线重合程度越高，两个变量的分布越相似
    # 计算拟合直线（最小二乘法）
    slope, intercept = np.polyfit(xr, yr, deg=1)
    # 生成直线的 y 值
    line = slope * xr + intercept
    # 绘制趋势线
    plt.plot(xr, line, color='red', linewidth=2)

    # ===================== 新增：参考线 =====================
    # 理想分布，和实际出入很大，不做详解
    # min_val = min(xr.min(), yr.min())
    # max_val = max(xr.max(), yr.max())
    # plt.plot([min_val, max_val], [min_val, max_val], 'k--', linewidth=1.5)


# 使用自定义函数创建QQ图
g = sns.FacetGrid(tips, hue="time", col="sex", height=4)
# 使用 map_dataframe，直接传入列名的字符串即可，Seaborn 会自动完成数据映射
g.map_dataframe(qqplot, x="total_bill", y="tip")

plt.show()