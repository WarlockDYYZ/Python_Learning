import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta


# ==================== 页面配置 ====================
st.set_page_config(
    page_title="电商销售分析面板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 数据层 ====================
@st.cache_data(ttl=3600)
def generate_mock_data(days=180, seed=42):
    np.random.seed(seed)
    categories = {
        "电子产品": ["智能手机", "笔记本电脑", "无线耳机", "智能手表", "平板电脑"],
        "服装": ["运动T恤", "牛仔裤", "羽绒服", "运动鞋", "连衣裙"],
        "食品": ["坚果礼盒", "进口牛奶", "有机大米", "休闲零食", "茶叶"],
        "家居": ["乳胶枕头", "智能台灯", "收纳箱", "空气净化器", "扫地机器人"],
        "美妆": ["精华液", "面膜套装", "口红", "防晒霜", "香水"]
    }
    channels = ["天猫", "京东", "抖音", "拼多多", "线下"]
    regions = ["广东", "浙江", "江苏", "北京", "上海", "四川", "湖北", "山东", "福建", "河南"]
    customer_types = ["新客", "老客"]

    n_orders = 5000
    start_date = datetime.now() - timedelta(days=days)
    all_dates = [start_date + timedelta(days=i) for i in range(days)]
    date_weights = [1.5 if d.weekday() >= 5 else 1.0 for d in all_dates]
    dates = np.random.choice(all_dates, size=n_orders, p=np.array(date_weights)/sum(date_weights))

    cat_list = np.random.choice(list(categories.keys()), size=n_orders, p=[0.3, 0.25, 0.15, 0.2, 0.1])
    products = [np.random.choice(categories[c]) for c in cat_list]

    df = pd.DataFrame({
        "order_id": [f"ORD{str(i).zfill(6)}" for i in range(n_orders)],
        "order_date": dates,
        "category": cat_list,
        "product_name": products,
        "channel": np.random.choice(channels, size=n_orders, p=[0.35, 0.25, 0.2, 0.12, 0.08]),
        "region": np.random.choice(regions, size=n_orders),
        "quantity": np.random.randint(1, 6, size=n_orders),
        "customer_type": np.random.choice(customer_types, size=n_orders, p=[0.3, 0.7])
    })
    price_map = {"电子产品": 800, "服装": 200, "食品": 80, "家居": 300, "美妆": 150}
    df["unit_price"] = df["category"].map(price_map) * np.random.uniform(0.7, 1.3, n_orders)
    df["unit_price"] = df["unit_price"].round(2)
    df["sales_amount"] = (df["quantity"] * df["unit_price"]).round(2)
    return df.sort_values("order_date").reset_index(drop=True)

def filter_data(df, date_range, categories, channels, regions):
    mask = (
        (df["order_date"].dt.date >= date_range[0]) &
        (df["order_date"].dt.date <= date_range[1]) &
        (df["category"].isin(categories)) &
        (df["channel"].isin(channels)) &
        (df["region"].isin(regions))
    )
    return df[mask].copy()

# ==================== 加载数据 ====================
df_raw = generate_mock_data()

# ==================== 侧边栏筛选 ====================
with st.sidebar:
    st.header("🔍 筛选条件")

    # 日期范围
    min_date = df_raw["order_date"].min().date()
    max_date = df_raw["order_date"].max().date()
    date_range = st.date_input(
        "选择日期范围",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # 品类
    categories = st.multiselect(
        "产品品类",
        options=sorted(df_raw["category"].unique()),
        default=sorted(df_raw["category"].unique())
    )

    # 渠道
    channels = st.multiselect(
        "销售渠道",
        options=sorted(df_raw["channel"].unique()),
        default=sorted(df_raw["channel"].unique())
    )

    # 地区
    regions = st.multiselect(
        "销售地区",
        options=sorted(df_raw["region"].unique()),
        default=sorted(df_raw["region"].unique())
    )

    st.divider()
    st.caption("💡 修改筛选条件后图表自动更新")

# ==================== 数据过滤 ====================
if len(date_range) == 2 and categories and channels and regions:
    df_filtered = filter_data(df_raw, date_range, categories, channels, regions)
else:
    st.warning("请至少选择一个品类、渠道和地区")
    st.stop()

# ==================== KPI 计算 ====================
total_sales = df_filtered["sales_amount"].sum()
total_orders = df_filtered["order_id"].nunique()
avg_order_value = total_sales / total_orders if total_orders > 0 else 0
new_cust_count = df_filtered[df_filtered["customer_type"] == "新客"]["order_id"].nunique()
new_cust_ratio = new_cust_count / total_orders * 100 if total_orders > 0 else 0

# ==================== 主内容区 ====================
st.title("📊 电商销售分析面板")
st.caption(f"数据范围：{date_range[0]} 至 {date_range[1]} | 共 {len(df_filtered)} 条订单记录")

# KPI 指标卡
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("总销售额", f"¥{total_sales:,.0f}", delta="+12.5%")
with col2:
    st.metric("订单总数", f"{total_orders:,}", delta="+8.3%")
with col3:
    st.metric("客单价", f"¥{avg_order_value:,.1f}", delta="+3.8%")
with col4:
    st.metric("新客占比", f"{new_cust_ratio:.1f}%", delta="-2.1%")

st.divider()

# ==================== 销售趋势图 ====================
st.subheader("📈 销售趋势分析")

trend_df = df_filtered.groupby(df_filtered["order_date"].dt.date).agg(
    销售额=("sales_amount", "sum"),
    订单数=("order_id", "nunique")
).reset_index()
trend_df.columns = ["日期", "销售额", "订单数"]

tab_trend1, tab_trend2 = st.tabs(["按日趋势", "按周汇总"])
with tab_trend1:
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Bar(x=trend_df["日期"], y=trend_df["销售额"],
                               name="销售额", yaxis="y", marker_color="#2E86DE"))
    fig_trend.add_trace(go.Scatter(x=trend_df["日期"], y=trend_df["订单数"],
                                   name="订单数", yaxis="y2", mode="lines+markers",
                                   line=dict(color="#E74C3C", width=2)))
    fig_trend.update_layout(
        yaxis=dict(title="销售额（元）"),
        yaxis2=dict(title="订单数", overlaying="y", side="right"),
        hovermode="x unified",
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_trend, width='stretch')

with tab_trend2:
    weekly_df = df_filtered.copy()
    weekly_df["周"] = weekly_df["order_date"].dt.isocalendar().week.astype(str) + "周"
    weekly = weekly_df.groupby("周")["sales_amount"].sum().reset_index()
    fig_week = px.bar(weekly, x="周", y="sales_amount", title="周度销售额",
                      color_discrete_sequence=["#2E86DE"])
    st.plotly_chart(fig_week, width='stretch')

st.divider()

# ==================== 品类与渠道分析 ====================
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🏷️ 品类销售占比")
    cat_sales = df_filtered.groupby("category")["sales_amount"].sum().sort_values(ascending=False).reset_index()
    fig_cat = px.pie(cat_sales, values="sales_amount", names="category", hole=0.4,
                     color_discrete_sequence=px.colors.qualitative.Set2)
    fig_cat.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig_cat, width='stretch')

with col_right:
    st.subheader("🛒 渠道销售分布")
    ch_sales = df_filtered.groupby("channel")["sales_amount"].sum().sort_values(ascending=True).reset_index()
    fig_ch = px.bar(ch_sales, x="sales_amount", y="channel", orientation="h",
                    color="channel", color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_ch.update_layout(showlegend=False, xaxis_title="销售额（元）")
    st.plotly_chart(fig_ch, width='stretch')

st.divider()

# ==================== 地区与商品排行 ====================
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("🗺️ 地区销售额排行")
    region_sales = df_filtered.groupby("region")["sales_amount"].sum().sort_values(ascending=False).reset_index()
    fig_region = px.bar(region_sales, x="region", y="sales_amount",
                        color="sales_amount", color_continuous_scale="Blues",
                        text_auto=".2s")
    fig_region.update_layout(xaxis_title="", yaxis_title="销售额（元）", showlegend=False)
    st.plotly_chart(fig_region, width='stretch')

with col_b:
    st.subheader("🏆 TOP 10 热销商品")
    top_products = df_filtered.groupby("product_name")["sales_amount"].sum().sort_values(ascending=False).head(10).reset_index()
    fig_top = px.bar(top_products.sort_values("sales_amount", ascending=True),
                     x="sales_amount", y="product_name", orientation="h",
                     color_discrete_sequence=["#27AE60"])
    fig_top.update_layout(yaxis_title="", xaxis_title="销售额（元）", height=400)
    st.plotly_chart(fig_top, width='stretch')

st.divider()

# ==================== 数据明细与导出 ====================
st.subheader("📋 数据明细")
with st.expander("展开查看完整数据（前100条）", expanded=False):
    st.dataframe(df_filtered.head(100), width='stretch')

csv_data = df_filtered.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    label="📥 导出筛选结果 CSV",
    data=csv_data,
    file_name=f"销售数据_{date_range[0]}_{date_range[1]}.csv",
    mime="text/csv"
)