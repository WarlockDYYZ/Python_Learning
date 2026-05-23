import altair as alt
from vega_datasets import data


# 加载数据
population = data.population()
print(population)


# 计算变换（transform_calculate）：创建新的计算字段
# 将性别代码转换为有意义的标签
alt.Chart(population).mark_bar().encode(
    x='year:O',         # X轴映射年份（Ordinal，有序分类）
    y='sum(people):Q',  # Y轴对人口数量进行求和聚合（Quantitative，定量）
    # color=alt.condition(
    #     alt.datum.sex == 1,
    #     alt.value('blue'),  # 如果sex=1，使用蓝色
    #     alt.value('red')    # 否则使用红色
    # )
    color='sex_label:N'  # 使用计算出的新标签来上色
).transform_calculate(
    sex_label="datum.sex == 1 ? 'Male' : 'Female'"
).save('transform_calculate.html')


# 过滤变换（transform_filter）：筛选数据
# 只显示男性人口数据
alt.Chart(population).mark_bar().encode(
    x='year:O',
    y='sum(people):Q'
).transform_filter(
    alt.datum.sex == 1
).save('transform_filter.html')


# 聚合变换（transform_aggregate）：创建聚合后的数据
# 计算每年的总人口
alt.Chart(population).mark_line().encode(
    x='year:T',                     # 重点1：将年份改为时间类型 (Temporal)
    y='total_people:Q'              # 重点2：使用 transform_aggregate 算出的新字段
).transform_aggregate(
    total_people='sum(people)',     # 重点3：必须给聚合结果起个名字！
    groupby=['year']                # 按年份分组
).save('transform_aggregate.html')
