import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 模拟生成股票数据：生成一只股票的30个交易日的收盘价和成交量数据
np.random.seed(42)
dates = pd.date_range('2023-01-01', periods=30, freq='D')
# 生成收盘价数据：以100元为基准，添加一个随机游走的波动，模拟真实股价的变化趋势
price = 100 + np.cumsum(np.random.normal(0.1, 1, 30))
# 生成成交量数据：在100万股到500万股之间随机波动
volume = np.random.randint(100, 500, 30)
stock_df = pd.DataFrame({
    'date': dates,
    'close': price,
    'volume': volume
})

# 2. 设时间索引，确保时间序列的语义正确
stock_df = stock_df.set_index('date').sort_index()

# 3. 计算技术指标（由于模拟数据只有一只股票，无需额外分组）
# 3.1 计算5日简单移动平均线（SMA）
stock_df['SMA_5'] = stock_df['close'].rolling(window=5).mean()
# 3.2 计算5日指数平滑移动平均线（EMA）
stock_df['EMA_5'] = stock_df['close'].ewm(span=5).mean()
# 3.3 计算布林带指标：中轨为5日SMA，上下轨为中轨±2倍的5日滚动标准差
stock_df['rolling_std'] = stock_df['close'].rolling(window=5).std()
stock_df['Upper_Band'] = stock_df['SMA_5'] + 2 * stock_df['rolling_std']
stock_df['Lower_Band'] = stock_df['SMA_5'] - 2 * stock_df['rolling_std']

# 4. 计算收益率指标
# 4.1 计算每日收益率：当日收盘价相对于前一日收盘价的涨跌幅
stock_df['daily_return'] = stock_df['close'].pct_change()
# 4.2 计算累计收益率：从第一个交易日到当日的总收益率
stock_df['cumulative_return'] = (1 + stock_df['daily_return']).cumprod() - 1

# 5. 打印计算结果，重点验证技术指标和收益率的计算是否正确
# noinspection PyTypeChecker
print(stock_df[['close', 'SMA_5', 'EMA_5', 'Upper_Band', 'Lower_Band', 'cumulative_return']].head(10).to_string())

# 6. 可视化：绘制收盘价、SMA、EMA、布林带
plt.figure(figsize=(12, 6))
plt.plot(stock_df.index, stock_df['close'], label='收盘价', alpha=0.8)
plt.plot(stock_df.index, stock_df['SMA_5'], label='5日简单移动平均', linestyle='--')
plt.plot(stock_df.index, stock_df['EMA_5'], label='5日指数移动平均', linestyle='--')
plt.fill_between(stock_df.index, stock_df['Upper_Band'], stock_df['Lower_Band'], color='gray', alpha=0.2, label='布林带区间')
plt.title('股票收盘价与核心技术指标')
plt.legend()
plt.show()