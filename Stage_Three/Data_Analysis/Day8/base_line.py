import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np


# 生成数据
df = pd.DataFrame({
    "日期": pd.date_range("2024-01-01", periods=30, freq="D"),
    "销售额": np.random.randint(100, 500, size=30).cumsum() // 10,
    "订单数": np.random.randint(20, 80, size=30)
})

# Plotly Express 折线图
fig = px.line(
    df,
    x="日期",
    y=["销售额", "订单数"],
    title="30天销售与订单趋势",
    labels={"value": "数值", "variable": "指标"},
    template="plotly_white"  # 主题：plotly, plotly_white, plotly_dark
)

# 自定义样式
fig.update_layout(
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# Streamlit 渲染
st.plotly_chart(fig, width="stretch")  # 自适应宽度