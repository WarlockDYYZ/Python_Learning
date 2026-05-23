import altair as alt
from vega_datasets import data


iris = data.iris()

# 1. 创建选择器（用于点击高亮数据点）
selection = alt.selection_point(fields=['species'])

chart = alt.Chart(iris).mark_circle(size=60).encode(
    x='petalLength:Q',
    y='petalWidth:Q',
    # 2. 鼠标悬停显示数据详情 (tooltip)
    tooltip=['species', 'petalLength', 'petalWidth'],
    # 3. 点击选择数据点：选中的保持原色，未选中的变为浅灰色
    color=alt.condition(selection, 'species:N', alt.value('lightgray'))
).add_params(
    selection  # 将选择器绑定到图表上
).properties(
    width='container',  # 宽度自适应容器
    height=400,
    title='鸢尾花花瓣长宽分布（支持点击与缩放）'
).interactive()  # 4. 开启缩放和平移功能


chart.save('altair_interactive.html')