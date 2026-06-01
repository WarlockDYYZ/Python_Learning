import pandas as pd


# 按理说是应该编一些数据的
df_left = pd.DataFrame()
df_right = pd.DataFrame()

# 内连接（默认）
merged_df = pd.merge(df_left, df_right, on='客户ID')
# 左连接
merged_df = pd.merge(
    df_left,
    df_right,
    on='客户ID',
    how='left'
)
# 右连接
merged_df = pd.merge(
df_left,
df_right,
on='客户ID',
how='right'
)
# 外连接
merged_df = pd.merge(
df_left,
df_right,
on='客户ID',
how='outer'
)
# 多键合并
merged_df = pd.merge(
df_left,
df_right,
left_on=['客户ID', '城市'],
right_on=['客户ID', '城市'],
how='inner'
)
# 添加合并来源指示
merged_df = pd.merge(
df_left,
df_right,
on='客户ID',
how='outer',
indicator=True # 添加'_merge'列指示来源
)


# 连接组合
df_orders = pd.DataFrame()
df_customers = pd.DataFrame()
try:
    merged_df = pd.merge(
        df_orders,
        df_customers,
        on='客户ID',
        how='left',
        validate='many_to_one'  # 明确告诉 Pandas：右边必须是一对一的唯一键
    )
except Exception as e:
    print(f"合并失败，数据质量有问题！原因：{e}")


# concat()方法
df1 = pd.DataFrame()
df2 = pd.DataFrame()
# 纵向合并（默认）
concatenated_df = pd.concat([df1, df2])
# 横向合并
concatenated_df = pd.concat([df1, df2], axis=1)
# 处理索引
concatenated_df = pd.concat([df1, df2], ignore_index=True)
# 添加层次索引
concatenated_df = pd.concat(
    [df1, df2],
    keys=['2025年', '2026年'],
    names=['年份', 'None']
)
