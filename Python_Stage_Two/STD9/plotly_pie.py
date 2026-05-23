import plotly.express as px


# 自定义数据
data = {
    'Fruit': ['Apples', 'Bananas', 'Oranges', 'Grapes'],
    'Amount': [35, 25, 20, 20]
}

# 创建饼图
fig = px.pie(
    data,
    values='Amount',
    names='Fruit',
    title='Fruit Distribution',
    color_discrete_sequence=px.colors.qualitative.Set3
)

fig.show()
