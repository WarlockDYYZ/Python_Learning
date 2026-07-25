import streamlit as st
import pandas as pd
import numpy as np


df = pd.DataFrame({
    "产品": ["A", "B", "C", "D"],
    "销量": [120, 340, 280, 450],
    "单价": [29.9, 59.9, 39.9, 99.9]
})

# 1. 交互式表格（可排序、调整列宽、全屏）
st.dataframe(df, width=600, height=200)

# 2. 静态表格（打印样式，不可交互）
st.table(df)

# 3. 数据编辑器（可编辑，返回修改后的数据）
edited_df = st.data_editor(df, num_rows="dynamic")
st.write("修改后的数据：", edited_df)

# 4. 单列高亮
st.dataframe(df.style.highlight_max(axis=0))


# JSON 数据展示
data = {"name": "销售报表", "version": "1.0", "metrics": {"gmv": 128000}}
st.json(data)

# 代码块展示
code = """
def calculate_gmv(sales_df):
    return (sales_df["销量"] * sales_df["单价"]).sum()
"""
st.code(code, language="python")