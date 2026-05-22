import altair as alt
from vega_datasets import data


# 加载数据
iris = data.iris()

# 创建图表，改变了一下大小
chart = alt.Chart(
    iris,
    width=600,   # 画布宽度
    height=400   # 画布高度
).mark_circle(size=80).encode(  # 散点大小
    x='petalLength',
    y='petalWidth',
    color='species'
)

chart.save('iris.html')
chart.show()