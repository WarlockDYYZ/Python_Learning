import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 创建数据
dates = pd.date_range('2023-01-01', periods=30)
np.random.seed(42)

# 生成OHLC数据
open_prices = 100 + np.cumsum(np.random.normal(0, 1, 30))
# 确保最高价不低于开盘和收盘，最低价不高于开盘和收盘
high_prices = np.maximum(open_prices, open_prices + np.random.normal(1, 0.5, 30))
low_prices = np.minimum(open_prices, open_prices - np.random.normal(1, 0.5, 30))
close_prices = open_prices + np.cumsum(np.random.normal(0, 0.5, 30))

# 2. 创建图表
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8),
                               sharex=True,
                               gridspec_kw={'height_ratios': [3, 1]})

# 3. 绘制K线（修复错位的核心部分）
for i, (open_p, high_p, low_p, close_p) in enumerate(zip(
        open_prices, high_prices, low_prices, close_prices)):
    # A股习惯：涨（收盘>=开盘）为红色，跌为绿色
    color = 'red' if close_p >= open_p else 'green'

    # 绘制上下影线（用细的黑线或同色线连接最高最低价）
    ax1.plot([i, i], [low_p, high_p], color=color, linewidth=1)

    # 绘制K线实体（用较粗的线段表示开盘到收盘）
    ax1.plot([i, i], [open_p, close_p], color=color, linewidth=4)

# 4. 设置主图样式
ax1.set_ylabel('价格', fontsize=12)
ax1.set_title('K线图示例', fontsize=16, fontweight='bold')
ax1.grid(True, alpha=0.3)
# 设置X轴刻度（每5天显示一个日期）
ax1.set_xticks(range(0, 30, 5))
ax1.set_xticklabels(dates[::5].strftime('%Y-%m-%d'), rotation=45)

# 5. 绘制成交量
# 提取每天的涨跌状态，生成对应的成交量颜色
colors = ['red' if close >= open else 'green' for open, close in zip(open_prices, close_prices)]
ax2.bar(range(30), np.random.randint(100000, 500000, 30), color=colors, alpha=0.7)

ax2.set_ylabel('成交量', fontsize=12)
ax2.set_xlabel('日期', fontsize=12)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()