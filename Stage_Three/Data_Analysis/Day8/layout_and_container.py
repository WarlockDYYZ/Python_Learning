import streamlit as st
import pandas as pd


# 侧边栏（Sidebar）
# 方式一：with 上下文管理器
with st.sidebar:
    st.title("筛选条件")
    category = st.selectbox("产品类别", ["全部", "电子", "服装", "食品"])
    date_range = st.date_input("日期范围")
    min_sales = st.slider("最低销售额", 0, 10000, 1000)
# 方式二：点语法（更简洁）
show_chart = st.sidebar.checkbox("显示图表", value=True)

# 主区域
st.title("销售分析看板")
st.write(f"当前筛选：{category}")


# 列布局（Columns）
# 三等分列
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("总销售额", "¥128,500", "+12.5%")
with col2:
    st.metric("订单数", "1,284", "+8.3%")
with col3:
    st.metric("客单价", "¥99.8", "-2.1%")

# 自定义宽度比例
col_left, col_right = st.columns([2, 1])  # 左宽右窄
with col_left:
    st.write("主图表区域")
with col_right:
    st.write("数据明细")


# 选项卡（Tabs）
tab1, tab2, tab3 = st.tabs(["销售概览", "产品分析", "客户画像"])

with tab1:
    st.header("销售概览")
    st.write("GMV、订单量、转化率等核心指标")
with tab2:
    st.header("产品分析")
    st.write("品类分布、TOP 商品、滞销分析")
with tab3:
    st.header("客户画像")
    st.write("地域分布、消费层级、复购率")


# 折叠面板（Expander）
with st.expander("高级筛选选项", expanded=False):
    st.checkbox("仅显示有库存商品")
    st.slider("利润空间", 0, 100, 30)
    st.multiselect("仓库", ["北京仓", "上海仓", "广州仓"])


# 容器（Container）与占位符
# 容器：逻辑分组，可后序往里追加内容
with st.container() as main_container:
    st.write("这是容器内的内容")

# 占位符：先占位置，后填充（适合异步加载场景）
placeholder = st.empty()

# 后续填充
some_df = pd.DataFrame({
    "产品": ["A", "B", "C", "D"],
    "销量": [120, 340, 280, 450],
    "单价": [29.9, 59.9, 39.9, 99.9]
})
placeholder.dataframe(some_df)
# 也可以清空，注释下面一行，就不显示 pandas 的数据了
placeholder.empty()