import altair as alt
from vega_datasets import data


# 加载数据
cars = data.cars()

# 创建直方图 (数据分箱)
alt.Chart(cars).mark_bar().encode(
    alt.X('Horsepower').bin(),  # 自动分箱
    y='count()'  # 统计每个箱的数量
).save('binning.html')


# 按原产地统计平均油耗 (聚合操作)
alt.Chart(cars).mark_bar().encode(
   x='Origin',
   y='mean(Miles_per_Gallon)'  # 计算平均值
).save('mean_miles_per_gallon.html')


# 按原产地和年份统计平均马力 (分组聚合)
alt.Chart(cars).mark_line().encode(
   x='Year',
   y='mean(Horsepower)',
   color='Origin'
).save('grouped_aggregation.html')
