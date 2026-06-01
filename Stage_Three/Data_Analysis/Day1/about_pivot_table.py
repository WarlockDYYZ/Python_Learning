import pandas as pd


# 编一个数据
df = pd.DataFrame()

# 基础透视表
pivot_table = pd.pivot_table(
    data=df,
    values=['销售额', '利润率'],
    index='产品',
    columns='地区',
    aggfunc={
            '销售额': 'sum',
            '利润率': 'mean'
        },
    fill_value=0,
    margins=True,
    margins_name='总计'
)

# 获取所有产品在“华东”地区的“销售额总和”这一整列
print(pivot_table[('华东', '销售额', 'sum')])
# 获取“产品A”在“华南”地区的“平均利润率”这一个具体的数值
print(pivot_table.loc['产品A', ('华南', '利润率', 'mean')])


# 按多层索引透视
df['年份'] = df['日期'].dt.year
df['季度'] = df['日期'].dt.quarter
df.set_index(['年份', '季度'], inplace=True)
# 创建多层透视表
pivot_table = pd.pivot_table(
    data=df,
    values='销售额',
    index=['年份', '季度'],
    columns='产品',
    aggfunc='sum',
    fill_value=0
)
# 处理透视表的多层索引
unstacked_pivot = pivot_table.unstack() # 展开索引
stacked_pivot = pivot_table.stack() # 合并索引
# 动态透视表
regions = df['地区'].unique().tolist()
products = df['产品'].unique().tolist()
dynamic_pivot = pd.pivot_table(
    data=df,
    values='销售额',
    index=['季度'],
    columns=['地区'],
    aggfunc='sum',
    fill_value=0,
    margins=True
)


# 基础交叉表
cross_table = pd.crosstab(index=df['季度'], columns=df['产品类别'])
print(cross_table)
# 输出：
# 产品类别 电子产品 家居用品 服装
# 季度
# Q1 15 10 5
# Q2 20 8 12
# 加权交叉表
cross_table_weighted = pd.crosstab(
index=df['季度'],
columns=df['产品类别'],
values=df['销售额'],
aggfunc='mean'
)


# 使用dropna参数
pivot_table = pd.pivot_table(
data=df,
values='销售额',
index='产品',
columns='地区',
aggfunc='sum',
fill_value=0,
margins=True,
dropna=False # 保留所有分组，即使某些地区没有销售
)
# 使用normalize参数
cross_table = pd.crosstab(
index=df['季度'],
columns=df['产品类别'],
normalize='index' # 按季度计算百分比
)