import streamlit as st
import plotly.express as px
import pandas as pd


# 1. 柱状图（各品类销售额）
category_df = pd.DataFrame({
    "品类": ["电子产品", "服装", "食品", "家居", "美妆"],
    "销售额": [45000, 32000, 28000, 38000, 22000],
    "同比增长": [0.15, 0.08, -0.03, 0.22, 0.31]
})

fig_bar = px.bar(
    category_df,
    x="品类",
    y="销售额",
    color="同比增长",
    color_continuous_scale="RdYlGn",
    text="销售额",
    title="各品类销售额对比"
)
fig_bar.update_traces(texttemplate="%{text:,}", textposition="outside")
st.plotly_chart(fig_bar, use_container_width=True)

# 2. 饼图（渠道占比）
channel_df = pd.DataFrame({
    "渠道": ["天猫", "京东", "抖音", "拼多多", "线下"],
    "占比": [35, 25, 20, 12, 8]
})
fig_pie = px.pie(
    channel_df,
    values="占比",
    names="渠道",
    title="销售渠道占比",
    hole=0.4  # 环形图
)
st.plotly_chart(fig_pie, use_container_width=True)

# 3. 散点图（客单价 vs 复购率）
scatter_df = pd.DataFrame({
    "客户群": ["高价值", "中产", "普通", "新客", "流失"],
    "客单价": [850, 420, 180, 150, 200],
    "复购率": [0.85, 0.62, 0.31, 0.15, 0.05],
    "人数": [1200, 3500, 8000, 5000, 2000]
})
fig_scatter = px.scatter(
    scatter_df,
    x="客单价",
    y="复购率",
    size="人数",
    color="客户群",
    title="客户价值矩阵",
    size_max=60
)
st.plotly_chart(fig_scatter, width="stretch")