import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px


# 1. 构造 customer_df
np.random.seed(42)  # 保证每次运行数据一致
n = 50

customer_df = pd.DataFrame({
    "客户ID": [f"C{str(i).zfill(4)}" for i in range(1, n + 1)],
    "客户群": np.random.choice(["高价值客户", "潜力客户", "流失风险", "新客户"], n),
    "地区": np.random.choice(["华东", "华南", "华北", "西南", "西北"], n),
    "等级": np.random.choice(["VIP", "金牌", "银牌", "普通"], n),
    "客单价": np.random.randint(100, 2000, n),
    "人数": np.random.randint(1, 20, n),
    "订单数": np.random.randint(1, 50, n),
    "复购率": np.round(np.random.uniform(0, 1, n), 2),
    "销售额": np.random.randint(500, 50000, n),
    "利润率": np.round(np.random.uniform(0.05, 0.45, n), 2),
    "最近消费时间": pd.date_range("2024-01-01", periods=n, freq="5D").strftime("%Y-%m-%d")
})


# 侧边栏选择图表维度
with st.sidebar:
    dim_x = st.selectbox("X轴维度", ["客单价", "人数", "订单数"])
    dim_y = st.selectbox("Y轴维度", ["复购率", "销售额", "利润率"])
    color_by = st.selectbox("颜色分组", ["客户群", "地区", "等级"])

# 动态生成图表
fig = px.scatter(
    customer_df,
    x=dim_x,
    y=dim_y,
    color=color_by,
    size="订单数",
    hover_data=["客户ID", "最近消费时间"],
    title=f"{dim_y} 随 {dim_x} 分布（按 {color_by} 分组）"
)
st.plotly_chart(fig, width="stretch")