import pandas as pd
import numpy as np


# 生成示例时间序列数据：覆盖2023年1月的逐日数据
np.random.seed(42)
dates = pd.date_range('2023-01-01', periods=10)
df = pd.DataFrame({
    'date': dates,
    'value': np.random.randint(10, 20, 10)  # 生成10-20范围内的随机整数
})

# 1. 整数窗口：计算连续3行数据的滚动均值
df['rolling_3'] = df['value'].rolling(window=3).mean()

# 2. 时间窗口：计算过去7天的滚动均值（需将时间列设为索引）
# 设置min_periods=1：只要窗口内有1个有效数据，就返回计算结果，避免开头处出现大量NaN
df['rolling_7d'] = df.set_index('date')['value'].rolling(
    window='7D',
    min_periods=1
).mean().values
print(df)


# Expanding Window
print("\n\n扩展窗口")
# 接上面的示例，计算扩展窗口的累计值
df['expanding_sum'] = df['value'].expanding().sum()  # 累计总和
df['expanding_mean'] = df['value'].expanding().mean()  # 累计平均值
# 验证结果：累计sum/累计mean 应等于当前行的value
print(df[['date', 'value', 'expanding_sum', 'expanding_mean']])


# exponentially weighted window
print("\n\n指数加权窗口")
# 接上面的示例，计算不同span下的指数加权移动平均
df['ewm_span5'] = df['value'].ewm(span=5).mean()  # 权重衰减较快，对近期数据更敏感
df['ewm_span10'] = df['value'].ewm(span=10).mean()  # 权重衰减较慢，曲线更平滑
# 计算普通滚动平均，用于对比
df['rolling_mean'] = df['value'].rolling(window=5).mean()

numeric_cols = ['value', 'rolling_mean', 'ewm_span5', 'ewm_span10']
df[numeric_cols] = df[numeric_cols].round(2)

# 仅对 float/int 类型的列四舍五入
# df_rounded = df.select_dtypes(include=['number']).round(2)
# 合并日期列后打印
# result = pd.concat([df[['date']], df_rounded], axis=1)

print(pd.concat([df[['date']], df[numeric_cols]], axis=1))