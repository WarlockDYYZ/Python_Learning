import altair as alt
from vega_datasets import data


population = data.population()

# 将性别代码转换为有意义的标签
alt.Chart(population).mark_bar().encode(
    x='year:O',
    y='sum(people):Q',
    color=alt.condition(
        alt.datum.sex == 1,
        alt.value('blue'),  # 如果sex=1，使用蓝色
        alt.value('red')    # 否则使用红色
    )
).transform_calculate(
     sex_label="datum.sex == 1 ? 'Male' : 'Female'"
).save('transform_calculate.html')
