import altair as alt
from vega_datasets import data


# 加载默认数据
cars = data.cars()
print(cars)

# 创建散点图
alt.Chart(cars).mark_circle().encode(
   x='Horsepower',
   y='Miles_per_Gallon',
   color='Origin',
   size='Weight_in_lbs'
).save('altair_scatter.html')
