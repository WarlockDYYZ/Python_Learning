import streamlit as st
import pandas as pd
import numpy as np

# 折线图与面积图
chart_data = pd.DataFrame(
    np.random.randn(20, 3).cumsum(axis=0),
    columns=["产品线A", "产品线B", "产品线C"],
    index=pd.date_range("2024-01-01", periods=20, freq="D")
)

# 折线图
st.line_chart(chart_data)
# 面积图
st.area_chart(chart_data)


# 柱状图与条形图
bar_data = pd.DataFrame({
    "品类": ["电子", "服装", "食品", "家居", "美妆"],
    "线上": [450, 320, 280, 380, 220],
    "线下": [180, 250, 320, 150, 90]
}).set_index("品类")

st.bar_chart(bar_data, horizontal=False)  # 垂直柱状图
# st.bar_chart(bar_data, horizontal=True)  # 水平条形图


# 散点图
scatter_data = pd.DataFrame({
    "x": np.random.randn(100),
    "y": np.random.randn(100),
    "size": np.random.randint(10, 100, 100),
    "color": np.random.choice(["A", "B", "C"], 100)
})

st.scatter_chart(
    scatter_data,
    x="x",
    y="y",
    size="size",
    color="color"
)


# 地图可视化
# 经纬度地图点
map_data = pd.DataFrame({
    "lat": [39.9042, 31.2304, 23.1291, 30.2741],  # 北京、上海、广州、杭州
    "lon": [116.4074, 121.4737, 113.2644, 120.1551],
    "销售额": [45000, 52000, 38000, 28000]
})

st.map(map_data, size="销售额")