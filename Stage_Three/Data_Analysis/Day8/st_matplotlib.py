import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# 解决中文显示问题
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 生成示例数据
dates = pd.date_range("2024-01-01", periods=12, freq="ME")
sales = np.random.randint(50, 200, size=12)

# 创建 Figure（推荐显式创建，避免全局状态污染）
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(dates, sales, marker="o", linewidth=2, color="#2E86DE")
ax.set_title("月度销售趋势", fontsize=14, fontweight="bold")
ax.set_xlabel("月份")
ax.set_ylabel("销售额（万元）")
ax.grid(alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()

# 传给 Streamlit 渲染
st.pyplot(fig)

# 关闭 figure 释放内存
plt.close(fig)