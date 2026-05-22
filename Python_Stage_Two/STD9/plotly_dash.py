import dash
from dash import dcc, html
import plotly.express as px


# 创建Dash应用
app = dash.Dash(__name__)

# 准备数据
df = px.data.gapminder().query("country=='Canada'")
# print(df)
# 表头：country continent  year  lifeExp       pop    gdpPercap iso_alpha  iso_num


# 创建布局
app.layout = html.Div([
    html.H1("Canada Life Expectancy Trend"),
    dcc.Graph(
        id='life-expectancy-chart',
        figure=px.line(df, x='year', y='lifeExp', title='Life Expectancy in Canada')
    )
])


if __name__ == '__main__':
    app.run(debug=True)