import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

# ================= 1. 数据准备 =================
# 构造示例数据，用于折线图、柱状图、饼图和热力图
df = pd.DataFrame({
    "月份": ["1月", "2月", "3月", "4月", "5月", "6月"] * 3,
    "销售额": [120, 150, 180, 160, 200, 220,
               90, 110, 130, 140, 170, 190,
               80, 100, 120, 150, 180, 210],
    "渠道": ["天猫"] * 6 + ["京东"] * 6 + ["抖音"] * 6
})

# ================= 2. 图表生成（基于你提供的代码） =================
# 1. 折线图：展示趋势变化
line_fig = px.line(
    df, x="月份", y="销售额", color="渠道",
    title="多渠道销售趋势对比",
    labels={"销售额": "销售额（万元）", "月份": "统计月份"},
    markers=True,
    template="plotly_white"
)

# 2. 柱状图：分组对比数据
bar_fig = px.bar(
    df, x="月份", y="销售额", color="渠道",
    barmode="group",
    title="各渠道月度销售额对比",
    text_auto=True
)

# 3. 饼图：展示占比分布
pie_fig = px.pie(
    df, values="销售额", names="渠道",
    title="各渠道销售额占比分布",
    hole=0.4
)

# 4. 热力图：展示矩阵类数据相关性
heatmap_fig = go.Figure(data=go.Heatmap(
    x=df["月份"], y=df["渠道"], z=df["销售额"],
    colorscale="Blues",
    text=df["销售额"],  # 修正：使用 text 参数显示单元格数值
    texttemplate="%{text}",
    zmin=0,
    zmax=df["销售额"].max()
))

# 5. 桑基图：展示用户行为流向
sankey_fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15, thickness=20, line=dict(color="black", width=0.5),
        label=["首页", "搜索页", "商品页", "加购页", "下单页", "支付页"]
    ),
    link=dict(
        source=[0, 0, 1, 1, 2, 3],
        target=[1, 2, 2, 3, 4, 5],
        value=[1000, 800, 600, 400, 300, 200]
    )
)])

# 6. 漏斗图：展示转化环节流失
funnel_fig = go.Figure(data=[go.Funnel(
    y=["首页", "商品页", "加购页", "下单页", "支付页"],
    x=[10000, 8000, 5000, 3000, 2000],
    textinfo="value+percent initial",
    marker_color=["#112233", "#445566", "#778899", "#aabbcc", "#ccdddd"]
)])

# ================= 3. Dash 页面布局 =================
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.layout = dbc.Container([
    html.H1("电商全链路数据分析看板", className="my-4 text-center"),

    # 第一行：折线图 + 柱状图
    dbc.Row([
        dbc.Col(dcc.Graph(figure=line_fig), width=6),
        dbc.Col(dcc.Graph(figure=bar_fig), width=6)
    ], className="mb-4"),

    # 第二行：饼图 + 热力图
    dbc.Row([
        dbc.Col(dcc.Graph(figure=pie_fig), width=6),
        dbc.Col(dcc.Graph(figure=heatmap_fig), width=6)
    ], className="mb-4"),

    # 第三行：桑基图 + 漏斗图
    dbc.Row([
        dbc.Col(dcc.Graph(figure=sankey_fig), width=6),
        dbc.Col(dcc.Graph(figure=funnel_fig), width=6)
    ])
], fluid=True)

if __name__ == '__main__':
    app.run(debug=True)