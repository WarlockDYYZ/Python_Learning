from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# 示例数据
df = pd.DataFrame({
    "月份": ["1月", "2月", "3月", "4月", "5月", "6月"],
    "销售额": [120, 150, 180, 160, 200, 220],
    "渠道": ["天猫", "京东", "抖音", "天猫", "京东", "抖音"]
})

# 布局设计
app.layout = dbc.Container([  # 响应式容器，自动适配屏幕宽度
    # 页面头部区域
    dbc.Row([
        dbc.Col(html.H1("电商销售分析报告"), width=12)
    ]),

    # 筛选栏区域：下拉选择器+日期范围选择器
    dbc.Row([
        dbc.Col([
            html.Label("选择渠道:"),
            dcc.Dropdown(
                id="channel-filter",
                options=[{"label": "全部渠道", "value": "all"}] + [{"label": c, "value": c} for c in df["渠道"].unique()],
                value="all",
                clearable=False,
                multi=True
            )
        ], width=6),
        dbc.Col([
            html.Label("选择日期范围:"),
            # 修复日期选择器
            dcc.DatePickerRange(
                id="date-range",
                start_date="2026-01-01",
                end_date="2026-06-30",
                display_format='YYYY-MM'
            )
        ], width=6)
    ], className="mt-4"),

    # 图表展示区域：选项卡分组不同分析维度
    dbc.Row([
        dbc.Col([
            dcc.Tabs(id="report-tabs", value="trend-tab", children=[
                dcc.Tab(label="销售趋势", value="trend-tab"),
                dcc.Tab(label="渠道对比", value="channel-tab")
            ]),
            html.Div(id="tab-content")
        ], width=12)
    ], className="mt-4"),

    # 数据表格区域
    dbc.Row([
        dbc.Col([
            html.H4("数据明细"),
            dash_table.DataTable(
                data=df.to_dict("records"),  # type: ignore
                page_size=10,
                style_table={"overflowX": "auto"},
                style_header={"backgroundColor": "#f8f9fa", "fontWeight": "bold"},
                style_data_conditional=[  # type: ignore
                    {
                        "if": {"filter_query": "{销售额} > 200"},
                        "backgroundColor": "#d4edda",
                        "color": "#155724"
                    }
                ]
            )
        ], width=12)
    ], className="mt-4")
])

if __name__ == '__main__':
    app.run(debug=True)