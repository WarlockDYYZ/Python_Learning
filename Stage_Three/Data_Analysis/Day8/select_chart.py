import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd


# 解决中文显示问题
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False


data = {
    "品类": ["电子产品", "电子产品", "电子产品", "服装", "服装", "服装", "家居", "家居", "家居"],
    "渠道": ["线上", "线下", "线上", "线下", "线上", "线下", "线上", "线下", "线上"],
    "销售额": [1200, 800, 1500, 600, 900, 700, 400, 550, 480]
}
df = pd.DataFrame(data)

# 侧边栏筛选
with st.sidebar:
    selected_cat = st.multiselect(
        "选择品类",
        options=df["品类"].unique(),
        default=df["品类"].unique()
    )
    chart_type = st.radio("图表类型", ["柱状图", "箱线图", "散点图"])

# 过滤数据
filtered_df = df[df["品类"].isin(selected_cat)]

# 根据选择渲染不同图表
fig, ax = plt.subplots(figsize=(10, 5))
if chart_type == "柱状图":
    sns.barplot(data=filtered_df, x="品类", y="销售额", ax=ax)
elif chart_type == "箱线图":
    sns.boxplot(data=filtered_df, x="品类", y="销售额", ax=ax)
else:
    sns.scatterplot(data=filtered_df, x="品类", y="销售额", hue="渠道", ax=ax)
st.pyplot(fig)
plt.close(fig)