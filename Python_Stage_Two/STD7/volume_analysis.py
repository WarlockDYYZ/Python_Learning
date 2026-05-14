import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号


# 创建数据
dates = pd.date_range('2023-01-01', periods=50)
np.random.seed(42)

# 生成价格和成交量数据
base_price = 100
prices = [base_price]
volumes = [200000]  # 👈 加一个初始值，长度变成 50，之前是空列表，因为 datas、prices，都是50而 volumes 是49，会报错
for i in range(1, 50):
    # 价格变化
    price_change = np.random.normal(0, 1.5)
    prices.append(prices[-1] + price_change)
    # 成交量（与价格变化相关）
    volume = 200000 + abs(price_change) * 50000 + np.random.normal(0, 20000)
    volumes.append(volume)

# 计算5日平均成交量
avg_volume = pd.Series(volumes).rolling(window=5).mean()

# ========== 关键：正确涨跌配色 ==========
colors = []
for i in range(len(prices)):
    if i == 0:
        colors.append('green')
    else:
        if prices[i] > prices[i-1]:
            colors.append('red')
        else:
            colors.append('green')

# 创建图表
fig, (ax1, ax2) = plt.subplots(
    2, 1,  # 2行1列布局，ax1 = 上图坐标轴、ax2 = 下图坐标轴
    figsize=(12, 8),
    sharex=True,  # 共享 X 轴（日期同步缩放）
    gridspec_kw={'height_ratios': [3, 1]}  # 上下高度比例 3:1
)

# 绘制价格，上图
ax1.plot(dates, prices, 'k-', linewidth=2, label='价格')
ax1.set_ylabel('价格', fontsize=12)   # Y 轴标题
ax1.set_title('股票价格与成交量分析', fontsize=16, fontweight='bold')  # 整个图表大标题
ax1.grid(True, alpha=0.3)  # 显示网格（淡灰色）
ax1.legend()

# 绘制成交量，下图
ax2.bar(dates, volumes, color=colors, alpha=0.7, label='成交量')
#  绘制 5 日平均成交量线，画在柱状图上面
ax2.plot(dates, avg_volume, 'b-', linewidth=2, label='5日平均成交量')
ax2.set_ylabel('成交量', fontsize=12)
ax2.set_xlabel('日期', fontsize=12)
ax2.legend()  # 显示图例
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()