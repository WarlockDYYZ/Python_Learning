import pandas as pd
import numpy as np
import statsmodels.api as sm

# 1. 构建典型不规则时序样本：15分钟级电力负荷数据，存在时间戳断点
rng = pd.date_range(start="2024-01-01", end="2024-01-07", freq="15min")
# 随机删除10%的时间戳，模拟采集缺失的真实场景
rng_missing = rng.delete(np.random.choice(len(rng), size=int(len(rng)*0.1), replace=False))
df = pd.DataFrame(
    {"power_load": np.random.normal(loc=1000, scale=50, size=len(rng_missing))},
    index=rng_missing
)
print("原始数据粒度：", df.index.freq)


# 场景：将15分钟级不规则数据，下采样为小时级数据
# 聚合逻辑：保留小时内的负荷最大值、最小值、平均值、区间起始值
downsampled_df = df.resample(rule="h", closed="left", label="left").agg(
    load_max=("power_load", "max"),
    load_min=("power_load", "min"),
    load_avg=("power_load", "mean"),
    load_start=("power_load", "first")
)
print("下采样后数据粒度：", downsampled_df.index.freq)
# print(downsampled_df)

# 进阶：对累计值时序的特殊聚合处理（如日级累计销量→月级总销量）
# 若直接对累计值做sum/mean会产生逻辑错误，需配合resample().last()提取区间终值
# 教程上这么写了，实际没有操作，等学完这一小节应该就知道要做什么了


# 场景：将小时级数据，上采样为5分钟级高频数据，补全缺失区间
upsampled_df = downsampled_df.resample("5min")
# print(upsampled_df.asfreq())  # 查看重采样生成的空客数据内容
# 插值方案分层选择，匹配不同时序特征：
# 1. 短区间缺失：时间加权线性插值（考虑索引的时间间隔，适配缓慢变化的平稳时序）
df_linear = upsampled_df.interpolate(method="time")
# print(df_linear)
# 2. 中区间缺失：样条插值（拟合曲线，保留非线性趋势）
df_spline = upsampled_df.interpolate(method="spline", order=3)
# print(df_spline)

# 3. 长区间缺失：结合Statsmodels STL分解的季节趋势插值
from statsmodels.tsa.seasonal import STL
# 先提取原始数据的季节项、趋势项
stl = STL(df["power_load"], period=24)  # 日周期：15分钟级×96=1天
res = stl.fit()
# 分别上采样到 5 分钟级
trend_upsample = res.trend.resample("5min").interpolate(method="time")
seasonal_upsample = res.seasonal.resample("5min").ffill()
resid_upsample = res.resid.resample("5min").interpolate(method="time")
# 重构数据
df_stl_interp = trend_upsample + seasonal_upsample + resid_upsample