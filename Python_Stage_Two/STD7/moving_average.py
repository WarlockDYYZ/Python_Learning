import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号


# 创建数据
dates = pd.date_range('2023-01-01', periods=100)
np.random.seed(42)

# 生成价格数据
prices = np.zeros(100)
prices[0] = 100
for i in range(1, 100):
    prices[i] = prices[i-1] + np.random.normal(0, 2)

# 计算移动平均线，5日、20日、60日
ma5 = pd.Series(prices).rolling(window=5).mean()
ma20 = pd.Series(prices).rolling(window=20).mean()
ma60 = pd.Series(prices).rolling(window=60).mean()

# 创建图表
fig, ax = plt.subplots(figsize=(12, 8))

# 绘制价格曲线
# 黑线，今日收盘价
ax.plot(dates, prices, 'k-', linewidth=1, label='收盘价')

# 绘制移动平均线
# 红色 5日、绿色 20日、蓝色 60日
ax.plot(dates, ma5, 'r-', linewidth=2, label='5日均线')
ax.plot(dates, ma20, 'g-', linewidth=2, label='20日均线')
ax.plot(dates, ma60, 'b-', linewidth=2, label='60日均线')

# 设置标题和标签
ax.set_title('股票价格与移动平均线', fontsize=16, fontweight='bold')
ax.set_xlabel('日期', fontsize=12)
ax.set_ylabel('价格', fontsize=12)

# 添加图例
ax.legend(loc='upper left')

# 添加网格
ax.grid(True, alpha=0.3)

# 自动调整 x 轴日期格式
# autofmt_xdate() → 解决日期重叠，自动倾斜、调整间距
plt.gcf().autofmt_xdate()
plt.tight_layout()
plt.show()