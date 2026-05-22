import plotly.express as px


# 创建3D散点图
df = px.data.iris()

fig = px.scatter_3d(
    df,
    x='sepal_length',
    y='sepal_width',
    z='petal_length',
    color='species',
    symbol='species'
)

fig.show()
