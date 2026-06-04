import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']
# 显示负号
plt.rcParams['axes.unicode_minus'] = False

# 1. 模拟生成高频传感器数据：每5分钟采集一次温度数据，连续采集2天
np.random.seed(42)
# 生成从2023-01-01 00:00:00开始的连续时间索引，频率为5分钟，共生成288个时间点（刚好覆盖1天）
dates = pd.date_range('2023-01-01', periods=288, freq='5min')
# 生成基础温度数据：以60度为基准，添加一个周期性的基础波动和随机噪音
temp = 60 + 5*np.sin(np.arange(288)*2*np.pi/48) + np.random.normal(0, 0.5, 288)
df = pd.DataFrame({'temperature': temp}, index=dates)
print(df.head())


# 2. 数据预处理：提取日期部分，用于后续分组
df['date'] = df.index.date
print(df.head())


# 3. 分组滚动计算：按日期分组，对每组使用30分钟的滚动窗口计算均值和标准差
# 窗口设置为'30min'，传感器数据的采集频率为5分钟，即每个窗口包含6个连续采集点
# min_periods=1：避免窗口开头出现大量NaN值
rolling_stats = (df.groupby('date')['temperature']
                 .rolling(window='30min', min_periods=1)
                 .agg(['mean', 'std'])
                 .reset_index(0, drop=True))  # 清理分组索引，将结果关联回原始DataFrame
# 一个多级行索引，看一下输出
# print(df.groupby('date')['temperature']
#                  .rolling(window='30min', min_periods=1)
#                  .agg(['mean', 'std']))
print(rolling_stats.head())


# 4. 将窗口计算结果合并回原始DataFrame
df['rolling_mean'] = rolling_stats['mean']
df['rolling_std'] = rolling_stats['std']

# 5. 异常值检测：温度值与滚动均值的偏差幅度超过3倍滚动标准差
# 3倍标准差是工业场景中常用的异常值检测阈值，符合正态分布的小概率事件判定逻辑
df['is_anomaly'] = abs(df['temperature'] - df['rolling_mean']) > 3 * df['rolling_std']

# 6. 筛选出异常值记录
anomalies = df[df['is_anomaly']]
print(f"检测到{len(anomalies)}条异常记录：")
# noinspection PyTypeChecker
print(anomalies[['temperature', 'rolling_mean', 'rolling_std']].head().to_string())

# 7. 可视化：对比原始温度曲线与滚动平均后的趋势曲线
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['temperature'], label='原始温度', alpha=0.5)
plt.plot(df.index, df['rolling_mean'], label='30分钟滚动平均', color='red')
plt.scatter(anomalies.index, anomalies['temperature'], color='red', label='异常值')
plt.title('设备温度监测与异常值检测')
plt.legend()
plt.show()