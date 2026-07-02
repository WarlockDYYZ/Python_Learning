import pandas as pd
import numpy as np
import statsmodels.api as sm

# 1. 构建典型不规则时序样本：15分钟级电力负荷数据，存在时间戳断点
rng = pd.date_range(start="2024-01-01", end="2024-01-07", freq="15T")
# 随机删除10%的时间戳，模拟采集缺失的真实场景
rng_missing = rng.delete(np.random.choice(len(rng), size=int(len(rng)*0.1), replace=False))
df = pd.DataFrame(
    {"power_load": np.random.normal(loc=1000, scale=50, size=len(rng_missing))},
    index=rng_missing
)
print("原始数据粒度：", df.index.freq)