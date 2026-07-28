import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st


# 解决中文显示问题
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 示例数据
df = pd.DataFrame({
    "品类": np.repeat(["电子", "服装", "食品", "家居"], 50),
    "销售额": np.concatenate([
        np.random.normal(150, 30, 50),
        np.random.normal(120, 25, 50),
        np.random.normal(80, 20, 50),
        np.random.normal(200, 40, 50)
    ]),
    "渠道": np.random.choice(["线上", "线下"], 200)
})

# 图1：箱线图
fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.boxplot(data=df, x="品类", y="销售额", hue="渠道", ax=ax1, palette="Set2")
ax1.set_title("各品类销售额分布")
st.pyplot(fig1)
plt.close(fig1)

# 图2：柱状图
fig2, ax2 = plt.subplots(figsize=(10, 5))
category_sales = df.groupby("品类")["销售额"].mean().sort_values(ascending=False)
sns.barplot(x=category_sales.index, y=category_sales.values, ax=ax2, palette="Blues_d")
ax2.set_title("各品类平均销售额")
for i, v in enumerate(category_sales.values):
    ax2.text(i, v + 2, f"{v:.0f}", ha="center")
st.pyplot(fig2)
plt.close(fig2)