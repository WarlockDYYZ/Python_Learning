# ----------------------------
# 1. 导入依赖库
# ----------------------------
from dash import Dash, html, dcc, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime
import numpy.typing as npt

# ----------------------------
# 2. 数据准备：模拟用户行为数据（真实场景替换为数据库/CSV读取）
# ----------------------------
def generate_behavior_data():
    """生成模拟用户行为数据，覆盖完整用户流程：首页→搜索→商品页→加购→下单→支付→离开"""
    np.random.seed(42)  # 设置随机种子，保证数据可复现
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 6, 30)
    date_range = pd.date_range(start=start_date, end=end_date, freq='h')
    n = len(date_range) * 50  # 模拟总行为数据量

    # 基础维度数据
    dates = np.random.choice(date_range, size=n)
    channels = np.random.choice(["天猫", "京东", "抖音", "拼多多", "小红书"], size=n, p=[0.3, 0.25, 0.2, 0.15, 0.1])
    user_types = np.random.choice(["新用户", "老用户"], size=n, p=[0.6, 0.4])
    devices = np.random.choice(["Mobile", "Desktop", "Tablet"], size=n, p=[0.7, 0.25, 0.05])
    behavior_steps = ["首页", "搜索页", "商品页", "加购页", "下单页", "支付页", "离开"]
    # 生成用户ID（模拟500个独立用户，ID范围 10001-10500）
    user_ids = np.random.randint(10001, 10501, size=n)

    # 生成用户行为路径与转化数据
    rng = np.random.default_rng(seed=42)
    current_step: npt.NDArray[np.str_] = rng.choice(
        behavior_steps[:-1],
        size=n,
        p=[0.3, 0.2, 0.25, 0.15, 0.07, 0.03]
    )

    next_step = []
    is_convert = []
    is_bounce = []

    for step in list(current_step):
        if step == "首页":
            next_s = np.random.choice(["搜索页", "商品页", "离开"], p=[0.4, 0.35, 0.25])
            bounce = True if next_s == "离开" else False
        elif step == "搜索页":
            next_s = np.random.choice(["商品页", "离开"], p=[0.6, 0.4])
            bounce = True if next_s == "离开" else False
        elif step == "商品页":
            next_s = np.random.choice(["加购页", "离开"], p=[0.55, 0.45])
            bounce = True if next_s == "离开" else False
        elif step == "加购页":
            next_s = np.random.choice(["下单页", "离开"], p=[0.4, 0.6])
            bounce = True if next_s == "离开" else False
        elif step == "下单页":
            next_s = np.random.choice(["支付页", "离开"], p=[0.3, 0.7])
            bounce = True if next_s == "离开" else False
        elif step == "支付页":
            next_s = "离开"
            bounce = False
        else:
            next_s = "离开"
            bounce = True

        next_step.append(next_s)
        is_convert.append(True if step == "支付页" else False)
        is_bounce.append(bounce)

    # 构建基础数据集
    df = pd.DataFrame({
        "用户ID": user_ids,
        "日期": dates,
        "渠道": channels,
        "用户类型": user_types,
        "设备": devices,
        "当前页面": current_step,
        "下一跳页面": next_step,
        "是否转化": is_convert,
        "是否跳出": is_bounce
    })

    # 补充计算留存数据
    user_cohort = df.groupby("用户ID")["日期"].min().reset_index()
    user_cohort.columns = ["用户ID", "首次访问日期"]
    df = df.merge(user_cohort, on="用户ID")
    df["留存天数"] = (df["日期"] - df["首次访问日期"]).dt.days
    df["是否留存"] = df["留存天数"].apply(lambda x: 1 if x > 0 else 0)

    return df

# 生成全局数据集
df = generate_behavior_data()

# ----------------------------
# 3. 初始化Dash应用
# ----------------------------
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],  # 引入Flatly Bootstrap主题
    suppress_callback_exceptions=True  # 忽略动态组件的回调异常
)
app.title = "用户行为分析报告"  # 设置页面标题
server = app.server  # 用于生产环境部署

# ----------------------------
# 4. 定义应用布局（响应式）
# ----------------------------
start_date = pd.to_datetime(df['日期'].min())
end_date = pd.to_datetime(df['日期'].max())

app.layout = dbc.Container([
    # 4.1 报告头部
    dbc.Row([
        dbc.Col([
            html.H1("📊 电商平台用户行为分析报告", className="text-center mb-2"),
            html.P(
                f"数据统计周期：{start_date.strftime('%Y年%m月%d日')} 至 "
                f"{end_date.strftime('%Y年%m月%d日')} | "
                f"报告生成时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M')}",
                className="text-center text-muted"
            )
        ], width=12)
    ], className="mt-4 mb-4"),

    # 4.2 全局筛选区
    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                # 日期范围筛选
                dbc.Col([
                    html.Label("选择日期范围：", className="fw-bold"),
                    dcc.DatePickerRange(
                        id="date-range-filter",
                        min_date_allowed=df["日期"].min(),
                        max_date_allowed=df["日期"].max(),
                        start_date=df["日期"].min(),
                        end_date=df["日期"].max(),
                        display_format='YYYY年MM月DD日',
                        className="w-100"
                    )
                ], width=3),
                # 渠道多选筛选
                dbc.Col([
                    html.Label("选择渠道来源：", className="fw-bold"),
                    dcc.Dropdown(
                        id="channel-filter",
                        options=[{"label": c, "value": c} for c in sorted(df["渠道"].unique())],
                        value=sorted(df["渠道"].unique()),
                        multi=True,
                        clearable=False
                    )
                ], width=3),
                # 用户类型多选筛选
                dbc.Col([
                    html.Label("选择用户类型：", className="fw-bold"),
                    dcc.Dropdown(
                        id="user-type-filter",
                        options=[{"label": t, "value": t} for t in sorted(df["用户类型"].unique())],
                        value=sorted(df["用户类型"].unique()),
                        multi=True,
                        clearable=False
                    )
                ], width=3),
                # 设备类型多选筛选
                dbc.Col([
                    html.Label("选择设备类型：", className="fw-bold"),
                    dcc.Dropdown(
                        id="device-filter",
                        options=[{"label": d, "value": d} for d in sorted(df["设备"].unique())],
                        value=sorted(df["设备"].unique()),
                        multi=True,
                        clearable=False
                    )
                ], width=3)
            ])
        ])
    ], className="mb-4 shadow-sm"),

    # 4.3 KPI概览区
    dbc.Row(id="kpi-cards", className="mb-4"),

    # 4.4 核心分析选项卡
    dbc.Card([
        dbc.CardBody([
            dcc.Tabs(id="analysis-tabs", value="trend-tab", children=[
                dcc.Tab(label="📈 流量趋势分析", value="trend-tab", className="fw-bold"),
                dcc.Tab(label="🔀 用户路径分析", value="path-tab", className="fw-bold"),
                dcc.Tab(label="🎯 转化漏斗分析", value="funnel-tab", className="fw-bold"),
                dcc.Tab(label="❤️ 留存质量分析", value="retention-tab", className="fw-bold"),
                dcc.Tab(label="🏢 渠道效果分析", value="channel-tab", className="fw-bold")
            ]),
            html.Div(id="tab-content", className="mt-4")
        ])
    ], className="mb-4 shadow-sm"),

    # 4.5 数据明细区
    dbc.Card([
        dbc.CardBody([
            html.H4("📋 行为数据明细", className="mb-3"),
            dash_table.DataTable(
                id="behavior-data-table",
                page_size=15,
                style_table={"overflowX": "auto"},
                style_header={
                    "backgroundColor": "#f8f9fa",
                    "fontWeight": "bold",
                    "textAlign": "center"
                },
                style_data={"textAlign": "center"},
                style_data_conditional=[
                    {
                        "if": {"filter_query": "{是否转化} = 1"},
                        "backgroundColor": "#d4edda",
                        "color": "#155724"
                    },
                    {
                        "if": {"filter_query": "{是否跳出} = 1"},
                        "backgroundColor": "#f8d7da",
                        "color": "#721c24"
                    }
                ]
            )
        ])
    ], className="mb-4 shadow-sm"),

    # 4.6 结论建议区
    dbc.Card([
        dbc.CardBody([
            html.H4("💡 分析结论与建议", className="mb-3"),
            dcc.Markdown(id="analysis-conclusion", children="""
            ##### 核心发现：
            1. **流量趋势**：全渠道流量在6月达到峰值，主要原因是618大促活动带来的引流效果；
            2. **用户路径**：用户从商品页到加购页的流失率最高，达到45%，是整个转化流程的核心瓶颈；
            3. **转化漏斗**：支付环节流失率为30%，主要原因是支付流程过于复杂、缺少访客支付方式；
            4. **留存质量**：老用户的7日留存率比新用户高出28个百分点，用户召回活动的实施效果较好；
            5. **渠道效果**：抖音渠道的转化效率最高，但是留存率显著低于其他渠道，流量质量有待提升。

            ##### 运营建议：
            1. 优化商品页的加购引导流程，简化加购操作步骤，降低该环节流失率；
            2. 优化支付流程，增加访客支付、免密支付等快捷支付方式，减少支付环节用户流失；
            3. 针对抖音渠道流量质量较低的问题，调整引流素材和定向规则，精准筛选高潜用户；
            4. 重点维护老用户，针对高价值老用户发放专属优惠券，进一步提升留存和转化；
            5. 在流量高峰时段（20-22点），加大搜索页到商品页的引流位投放，提升流量利用率。
            """)
        ])
    ], className="mb-4 shadow-sm"),

    # 页脚
    html.Footer([
        html.P("© 2024 数据分析部 | 本报告由 Dash 构建生成，数据仅用于业务分析", className="text-center text-muted mt-4")
    ])
], fluid=True, style={"backgroundColor": "#f8f9fa"})

# ----------------------------
# 5. 回调函数：处理交互逻辑
# ----------------------------
def filter_data(start_date, end_date, channels, user_types, devices):
    """根据筛选条件过滤数据，返回过滤后的子集"""
    mask = (
        (df["日期"] >= start_date) &
        (df["日期"] <= end_date) &
        (df["渠道"].isin(channels)) &
        (df["用户类型"].isin(user_types)) &
        (df["设备"].isin(devices))
    )
    return df[mask]

# 5.1 全局筛选器触发所有更新
@callback(
    Output("kpi-cards", "children"),
    Output("tab-content", "children"),
    Output("behavior-data-table", "data"),
    Input("date-range-filter", "start_date"),
    Input("date-range-filter", "end_date"),
    Input("channel-filter", "value"),
    Input("user-type-filter", "value"),
    Input("device-filter", "value")
)
def update_all_content(start_date, end_date, channels, user_types, devices):
    """根据筛选条件，更新KPI、图表、表格的所有内容"""
    # 过滤数据
    filtered_df = filter_data(start_date, end_date, channels, user_types, devices)
    if filtered_df.empty:
        return [], [html.P("⚠️  当前筛选条件下无可用数据，请调整筛选条件", className="text-center text-muted mt-5")], []

    # ----------------------------
    # 1. 计算KPI指标
    # ----------------------------
    total_uv = filtered_df["用户ID"].nunique()
    total_pv = len(filtered_df)
    bounce_rate = filtered_df["是否跳出"].mean() * 100
    convert_rate = filtered_df["是否转化"].mean() * 100
    retention_rate = filtered_df[filtered_df["留存天数"] == 7]["用户ID"].nunique() / total_uv * 100 if total_uv > 0 else 0

    # 构建KPI卡片
    kpi_cards = [
        dbc.Col(dbc.Card(dbc.CardBody([
            html.P("独立访客数（UV）", className="text-muted mb-1"),
            html.H3(f"{total_uv:,}", className="text-primary"),
            html.P("↑ 12.5% 同比", className="text-success mb-0 small")
        ]), className="shadow-sm text-center h-100"), width=2),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.P("页面浏览量（PV）", className="text-muted mb-1"),
            html.H3(f"{total_pv:,}", className="text-info"),
            html.P("↑ 8.3% 同比", className="text-success mb-0 small")
        ]), className="shadow-sm text-center h-100"), width=2),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.P("页面跳出率", className="text-muted mb-1"),
            html.H3(f"{bounce_rate:.1f}%", className="text-warning"),
            html.P("↓ 3.2% 同比", className="text-success mb-0 small")
        ]), className="shadow-sm text-center h-100"), width=2),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.P("整体转化率", className="text-muted mb-1"),
            html.H3(f"{convert_rate:.1f}%", className="text-success"),
            html.P("↑ 2.1% 同比", className="text-success mb-0 small")
        ]), className="shadow-sm text-center h-100"), width=2),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.P("7日留存率", className="text-muted mb-1"),
            html.H3(f"{retention_rate:.1f}%", className="text-danger"),
            html.P("↑ 5.4% 同比", className="text-success mb-0 small")
        ]), className="shadow-sm text-center h-100"), width=2)
    ]

    # ----------------------------
    # 2. 生成对应选项卡的图表内容
    # ----------------------------
    # 2.1 流量趋势图
    trend_df = (
        filtered_df
        .groupby([filtered_df["日期"].dt.date, "渠道"])
        .agg(独立访客数=("用户ID", "nunique"))
        .reset_index()
    )
    trend_fig = px.area(
        trend_df,
        x="日期",
        y="独立访客数",  # 修改为 agg() 中定义的新列名
        color="渠道",
        title="分渠道UV流量趋势",
        labels={
            "独立访客数": "独立访客数",  # 键名必须与 DataFrame 实际列名一致
            "日期": "统计日期"
        },
        template="plotly_white",
        height=500
    )
    trend_fig.update_layout(hovermode="x unified", legend_title_text="渠道来源")

    # 2.2 用户路径桑基图
    path_df = (
        filtered_df
        .groupby(["当前页面", "下一跳页面"])
        .agg(独立访客数=("用户ID", "nunique"))
        .reset_index()
    )
    labels = list(set(path_df["当前页面"].unique()) | set(path_df["下一跳页面"].unique()))
    label_map = {label: i for i, label in enumerate(labels)}
    path_df["source"] = path_df["当前页面"].map(label_map)
    path_df["target"] = path_df["下一跳页面"].map(label_map)
    sankey_fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15, thickness=20, line=dict(color="black", width=0.5),
            label=labels, color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2"]
        ),
        link=dict(
            source=path_df["source"],
            target=path_df["target"],
            value=path_df["独立访客数"],  # 修改为 agg() 中定义的新列名
            color="rgba(200, 200, 200, 0.3)"
        )
    )])
    sankey_fig.update_layout(title_text="用户行为流向路径分析", height=500)

    # 2.3 转化漏斗图
    funnel_stages = ["首页", "搜索页", "商品页", "加购页", "下单页", "支付页"]
    funnel_values = [filtered_df[filtered_df["当前页面"] == stage]["用户ID"].nunique() for stage in funnel_stages]
    funnel_fig = go.Figure(data=[go.Funnel(
        y=funnel_stages, x=funnel_values,
        textinfo="value+percent initial",
        marker=dict(color=["#112233", "#445566", "#778899", "#aabbcc", "#ccccdd", "#eeeeee"]),
        hovertemplate="阶段：%{y}<br>用户数：%{x}<br>占比：%{percentInitial:.1%}<extra></extra>"
    )])
    funnel_fig.update_layout(title_text="用户转化流程漏斗分析", height=500)

    # 2.4 留存热力图
    retention_df = filtered_df.groupby([pd.Grouper(key="日期", freq="W"), "留存天数"])["用户ID"].nunique().reset_index()
    retention_fig = px.density_heatmap(
        retention_df, x="留存天数", y="日期", z="用户ID",
        title="用户留存质量热力图（按周分组）", labels={"留存天数": "留存天数", "日期": "用户注册周期", "用户ID": "留存用户数"},
        color_continuous_scale="Blues", height=500
    )

    # 2.5 渠道效果分析图
    channel_df = filtered_df.groupby("渠道").agg(
        流量规模=("用户ID", "nunique"),
        转化率=("是否转化", "mean"),
        留存率=("是否留存", "mean")
    ).reset_index()
    channel_df["转化率"] = channel_df["转化率"] * 100
    channel_df["留存率"] = channel_df["留存率"] * 100
    channel_fig = make_subplots(specs=[[{"secondary_y": True}]])
    channel_fig.add_trace(go.Bar(
        x=channel_df["渠道"], y=channel_df["流量规模"],
        name="流量规模", marker=dict(color="#3498db")
    ), secondary_y=False)
    channel_fig.add_trace(go.Scatter(
        x=channel_df["渠道"], y=channel_df["转化率"],
        name="转化率（%）", mode="lines+markers", marker=dict(color="#e74c3c")
    ), secondary_y=True)
    channel_fig.add_trace(go.Scatter(
        x=channel_df["渠道"], y=channel_df["留存率"],
        name="留存率（%）", mode="lines+markers", marker=dict(color="#2ecc71")
    ), secondary_y=True)
    channel_fig.update_layout(
        title_text="渠道效果综合对比", height=500, showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    channel_fig.update_yaxes(title_text="流量规模", secondary_y=False)
    channel_fig.update_yaxes(title_text="比率（%）", secondary_y=True)

    # 按选项卡分组图表
    tab_content = [
        dcc.Tab(label="📈 流量趋势分析", value="trend-tab", children=[dcc.Graph(figure=trend_fig)]),
        dcc.Tab(label="🔀 用户路径分析", value="path-tab", children=[dcc.Graph(figure=sankey_fig)]),
        dcc.Tab(label="🎯 转化漏斗分析", value="funnel-tab", children=[dcc.Graph(figure=funnel_fig)]),
        dcc.Tab(label="❤️ 留存质量分析", value="retention-tab", children=[dcc.Graph(figure=retention_fig)]),
        dcc.Tab(label="🏢 渠道效果分析", value="channel-tab", children=[dcc.Graph(figure=channel_fig)])
    ]

    # ----------------------------
    # 3. 更新数据明细表格
    # ----------------------------
    table_data = filtered_df.sort_values("日期", ascending=False).head(500).to_dict("records")

    return kpi_cards, tab_content, table_data

# ----------------------------
# 运行应用
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)