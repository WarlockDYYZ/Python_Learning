import altair as alt
from vega_datasets import data


# 注册并启用自定义主题
@alt.theme.register('custom_theme',enable=True)
def custom_theme_registered():
    return {
            "view": {"width": 600, "height": 400},
            "axis": {
                "labelFontSize": 12,
                "titleFontSize": 14,
                "titleFontWeight": "bold"
            },
            "legend": {
                "labelFontSize": 11,
                "titleFontSize": 12
            },
            "mark": {"color": "#1f77b4"}
        }

# 启用主题
alt.theme.enable('custom_theme')

# 展示主题的绘图代码
# 加载汽车数据集
cars = data.cars()

# 绘制散点图 + 线性回归线
# 因为启用了自定义主题，这里的散点和线条会自动应用 #1f77b4 颜色
chart = alt.Chart(cars).mark_circle().encode(
    x=alt.X('Horsepower:Q', title='马力 (Horsepower)'),
    y=alt.Y('Miles_per_Gallon:Q', title='每加仑英里数 (MPG)'),
    tooltip=['Name', 'Horsepower', 'Miles_per_Gallon']
).properties(
    title='汽车马力与油耗关系图'  # 标题也会受到主题中 axis 字体配置的影响
)

# 添加一条线性回归线（同样会受主题默认颜色影响）
line = chart.transform_regression('Horsepower', 'Miles_per_Gallon').mark_line()

# 合并图表并显示
(chart + line).save('my_chart.html')