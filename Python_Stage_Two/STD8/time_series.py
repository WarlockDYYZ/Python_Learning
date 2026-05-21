import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# 设置全局字体为“微软雅黑”（Windows系统自带）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# 解决负号显示成方块的问题
plt.rcParams['axes.unicode_minus'] = False
# 加载数据集
tips = sns.load_dataset("tips")
# print(tips)
flights = sns.load_dataset("flights")


# 伪造一个日期列（假设数据是从 2024-01-01 开始的连续记录）
tips['date'] = pd.date_range(start='2026-01-01', periods=len(tips), freq='D')

# 加载时间序列数据
tips['date'] = pd.to_datetime(tips['date'])
# 按时间分组的统计
daily_tips = tips.groupby('date')['tip'].agg(['mean', 'count']).reset_index()
print(daily_tips)
# 绘制时间序列(基础的就不看了)
# sns.lineplot(data=daily_tips, x='date', y='mean')

sns.lineplot(
    data=daily_tips,          # 直接使用原始数据
    x='date',
    y='mean',            # Y轴直接放 tip
    errorbar='sd',      # Seaborn 会自动按 date 分组，并计算每天 tip 的标准差画出阴影
    marker='*'
)

plt.show()


# 复杂时间序列分析
# 多序列时间图
sns.lineplot(
    data=flights,
    x="month", y="passengers",
    hue="year",
    marker="o",
    linewidth=2
    # ,legend='full'  # 加上这个参数，强制显示所有年份
)

plt.tight_layout()
plt.show()


# 时间序列热力图
flights_wide = flights.pivot(index="year", columns="month", values="passengers")
sns.heatmap(
    flights_wide,
    annot=True, fmt="d",
    cmap="YlGnBu",
    linewidths=0.5
)
plt.show()
