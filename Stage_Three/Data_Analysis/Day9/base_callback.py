from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# 模拟数据
df = pd.DataFrame({
    "月份": ["1月", "2月", "3月", "4月", "5月", "6月"],
    "销售额": [120, 150, 180, 160, 200, 220],
    "渠道": ["天猫", "京东", "抖音", "天猫", "京东", "抖音"]
})

# 布局：下拉框+图表
app.layout = html.Div([
    html.H1("渠道销售趋势分析"),
    html.Label("选择分析渠道:"),
    dcc.Dropdown(
        id="channel-selector",
        options=[{"label": "全部渠道", "value": "all"}] + [{"label": c, "value": c} for c in df["渠道"].unique()],
        value="all",
        clearable=False
    ),
    dcc.Graph(id="sales-trend-chart")  # 图表容器，初始状态无内容
])

# 回调函数：下拉框输入变化，更新图表的figure属性
@callback(
    Output("sales-trend-chart", "figure"),  # 输出：指定图表组件的figure属性
    Input("channel-selector", "value")  # 输入：指定下拉框组件的value属性
)
def update_chart(selected_channel):
    """根据用户选择的渠道，动态更新图表"""
    # 数据筛选逻辑
    if selected_channel == "all":
        filtered_df = df
        title = "全渠道销售趋势"
    else:
        filtered_df = df[df["渠道"] == selected_channel]
        title = f"{selected_channel}销售趋势"

    # 生成新图表
    fig = px.line(
        filtered_df,
        x="月份",
        y="销售额",
        color="渠道",
        title=title,
        markers=True  # 折线图上显示数据节点标记
    )
    return fig  # 将图表对象返回给输出组件，完成更新

if __name__ == '__main__':
    app.run(debug=True)