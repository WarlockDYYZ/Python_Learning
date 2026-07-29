import plotly.graph_objects as go
import streamlit as st
import pandas as pd


category_df = pd.DataFrame({
    "品类": ["电子产品", "服装", "食品", "家居", "美妆"],
    "销售额": [45000, 32000, 28000, 38000, 22000],
    "同比增长": [0.15, 0.08, -0.03, 0.22, 0.31]
})

fig = go.Figure()
fig.add_trace(go.Bar(x=category_df["品类"], y=category_df["销售额"], name="销售额"))
fig.add_trace(go.Scatter(x=category_df["品类"], y=category_df["同比增长"]*100000,
                         name="增长率", yaxis="y2", mode="lines+markers"))
fig.update_layout(
    yaxis=dict(title="销售额"),
    yaxis2=dict(title="增长率(%)", overlaying="y", side="right"),
    title="双Y轴组合图"
)
st.plotly_chart(fig, width="stretch")