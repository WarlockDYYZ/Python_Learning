import seaborn as sns


# 1. 读取数据
df_long = sns.load_dataset("flights")

print("===== 长格式数据 =====")
print(df_long.head(10))
print("形状：", df_long.shape)


# 2. pivot 长 → 宽
df_wide = df_long.pivot(index="year", columns="month", values="passengers")

print("\n===== 宽格式数据 =====")
print(df_wide.head())
print("形状：", df_wide.shape)


# 3. melt 宽 → 长
df_back_long = df_wide.reset_index().melt(
    id_vars="year",
    var_name="month",
    value_name="passengers"
)

print("\n===== 转回长格式 =====")
print(df_back_long.head(10))
print("形状：", df_back_long.shape)
