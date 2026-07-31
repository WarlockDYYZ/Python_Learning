import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc

# 1. 数据准备
# 构造包含真实日期格式的示例数据，以支持日期范围筛选
df = pd.DataFrame({
    "月份": ["1月", "2月", "3月", "4月", "5月", "6月"],
    "日期": pd.to_datetime(["2024-01-01", "2024-02-01", "2024-03-01",
                            "2024-04-01", "2024-05-01", "2024-06-01"]),
    "销售额": [120, 150, 180, 160, 200, 220],
    "渠道": ["天猫", "京东", "抖音", "天猫", "京东", "抖音"]
})

# 2. 页面布局
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.layout = dbc.Container([
    html.H2("电商销售数据看板", className="my-4"),

    # 筛选组件（ID 必须与回调中的 Input 严格对应）
    dbc.Row([
        dbc.Col([
            html.Label("选择渠道:"),
            dcc.Dropdown(
                id="channel-selector",  # 对应回调中的 channel-selector
                options=[{"label": "全部渠道", "value": "all"}] +
                        [{"label": c, "value": c} for c in df["渠道"].unique()],
                value="all",
                clearable=False
            )
        ], width=6),
        dbc.Col([
            html.Label("选择日期范围:"),
            dcc.DatePickerRange(
                id="date-range",  # 对应回调中的 date-range
                start_date=df["日期"].min(),
                end_date=df["日期"].max(),
                display_format='YYYY-MM-DD'
            )
        ], width=6)
    ]),

    # 图表展示区
    dbc.Row([
        dbc.Col(dcc.Graph(id="sales-trend-chart"), width=8),  # 对应 Output 1
        dbc.Col(html.H4(id="chart-summary"), width=4)  # 对应 Output 2
    ], className="mt-4")
])


# 3. 回调逻辑
@callback(
    Output("sales-trend-chart", "figure"),
    Output("chart-summary", "children"),
    Input("channel-selector", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date")
)
def update_multi_outputs(selected_channel, start_date, end_date):
    # 1. 处理空值或无效输入
    if not start_date or not end_date:
        return px.line(title="请选择日期范围"), "暂无统计数据"

    # 2. 按日期范围筛选数据
    filtered_df = df[(df["日期"] >= start_date) & (df["日期"] <= end_date)].copy()

    # 3. 按渠道筛选（兼容单选和多选）
    if selected_channel and selected_channel != "all":
        # 如果 Dropdown 开启了 multi=True，selected_channel 会是列表，需用 isin
        if isinstance(selected_channel, list):
            filtered_df = filtered_df[filtered_df["渠道"].isin(selected_channel)]
        else:
            filtered_df = filtered_df[filtered_df["渠道"] == selected_channel]

    # 4. 生成新图表
    fig = px.line(
        filtered_df,
        x="月份",
        y="销售额",
        color="渠道",
        title="销售额趋势图",
        markers=True
    )

    # 5. 生成统计文本
    total_sales = filtered_df["销售额"].sum()
    summary = f"统计周期内总销售额：¥{total_sales:,.2f}"

    # 6. 按顺序返回多个输出
    return fig, summary


if __name__ == '__main__':
    app.run(debug=True)