import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# 生成模拟股票数据
dates = pd.date_range('2023-01-01', periods=252)
np.random.seed(42)

# 模拟股价（带趋势）
base_price = 100
returns = np.random.normal(0, 0.01, 252)
returns[0] = 0  # 确保第一个值为100
cumulative_returns = np.cumsum(returns)
prices = base_price * np.exp(cumulative_returns)

# 创建DataFrame
stock_data = pd.DataFrame({
    'Open': prices + np.random.normal(0, 0.5, 252),  # 开盘价
    'High': prices + np.random.normal(0, 1, 252),    # 最高价
    'Low': prices - np.random.normal(0, 1, 252),     # 最低价
    'Close': prices,                                                # 收盘价
    'Volume': np.random.randint(100000, 500000, 252)                # 成交量
}, index=dates)  # # 日期作为索引（mplfinance强制要求）

# 绘制K线图（需要mplfinance配合）
import mplfinance as mpf

# 设置中国股市风格（红涨绿跌）
marketcolors = mpf.make_marketcolors(
    up='red',      # 上涨 → 红色
    down='green',  # 下跌 → 绿色
    edge='inherit',
    wick='inherit'
)
style = mpf.make_mpf_style(marketcolors=marketcolors)

# 绘制K线图
mpf.plot(
    stock_data,
    type='candle',   # 画蜡烛图（K线）
    style=style,     # 红涨绿跌
    mav=(5, 20),     # 5日、20日均线
    volume=True,
    figsize=(12, 8)
)

plt.show()
