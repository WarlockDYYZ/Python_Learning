import plotly.express as px
import pandas as pd

# 创建散点图
df = px.data.iris()

fig = px.scatter(
    df,
    x="sepal_width",
    y="sepal_length",
    color="species"
)

fig.show()
