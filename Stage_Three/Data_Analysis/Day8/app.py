import streamlit as st


# 页面标题
st.title("我的第一个 Streamlit 应用")

# 普通文本
st.write("欢迎来到 Streamlit 交互式数据分析世界！")

# Markdown 支持
st.markdown("## 这是二级标题")
st.markdown("**加粗** 和 *斜体* 都支持")

# 显示数据
import pandas as pd
df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五"],
    "销售额": [1200, 3400, 2800]
})
st.dataframe(df)