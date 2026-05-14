import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
import numpy as np

# 设置中文字体（mplfinance需要特殊处理）
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 创建示例数据
# 生成一组连续的日期，生成 30 天
dates = pd.date_range('2023-01-01', periods=30)
np.random.seed(42)

# 生成价格数据
base_price = 100
prices = [base_price]
for i in range(1, 30):
    # 生成正态分布随机数（均值 0，波动 2）
    change = np.random.normal(0, 2)
    prices.append(prices[-1] + change)

# 创建DataFrame
# 创建 K 线必须的表格
# 必须包含：Open、High、Low、Close、Volume
df = pd.DataFrame({
    'Open': np.array(prices[:-1]) + np.random.normal(0, 1, 29),
    'High': np.array(prices[:-1]) + np.random.normal(0, 2, 29),  # 30个
    'Low': np.array(prices[:-1]) - np.random.normal(0, 2, 29),   # 30个
    'Close': prices[1:],
    'Volume': np.random.randint(100000, 500000, 29)
}, index=dates[1:])  # 行索引是日期（29 天）

# 设置中国股市风格（红涨绿跌）
marketcolors = mpf.make_marketcolors(
    up='red',
    down='green',
    edge='inherit',
    wick='inherit'
)

style = mpf.make_mpf_style(
    marketcolors=marketcolors,
    figcolor='white',
    gridcolor='gray',
    rc={'font.family': 'SimHei', 'axes.unicode_minus': False}
)

# 绘制K线图
fig, axes = mpf.plot(
    df,  # 必传：K线标准DataFrame
    type='candle',  # 图表类型
    style=style,  # 整体外观风格
    mav=(5, 20),  # 多条移动平均线，蓝色 橘黄色
    volume=True,  # 是否显示成交量副图
    returnfig=True,  # 是否返回画布和坐标轴
    figsize=(12, 8),  # 画布尺寸
    figscale=1.2,  # 整体缩放比例
    figratio=(12, 8),  # 画布宽高比例
    # title='股票K线走势',   # 简易标题（不用returnfig也能加）
    # show_nontrading=False, # 不显示非交易日（周末、节假日断开）
    # tight_layout=True,     # 自动紧凑布局
    # volume_panel=1,        # 成交量放在第几个面板
)

# 添加标题
axes[0].set_title('股票K线图示例', fontsize=16, fontweight='bold')
# mplfinance 画图 → 不要用 plt.tight_layout()
# plt.tight_layout()
plt.show()