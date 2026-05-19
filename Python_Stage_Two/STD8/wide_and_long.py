import seaborn as sns
import pandas as pd

# 1. 加载原生长格式数据集
df_long = sns.load_dataset("flights")
print("========== 原始 长格式数据 ==========")
print(df_long.head(10))
print(f"形状：{df_long.shape}\n")

# 2. pivot 长格式 → 宽格式
df_wide = df_long.pivot(index="year", columns="month", values="passengers")
print("========== pivot 转为 宽格式数据 ==========")
print(df_wide.head())
print(f"形状：{df_wide.shape}\n")

# 3. melt 宽格式 → 转回长格式
df_back_long = df_wide.reset_index().melt(
    id_vars="year",
    var_name="month",
    value_name="passengers"
)
print("========== melt 转回 长格式数据 ==========")
print(df_back_long.head(10))
print(f"形状：{df_back_long.shape}")