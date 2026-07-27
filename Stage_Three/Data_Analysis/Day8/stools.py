import streamlit as st


# 滑块与数字输
# 整数滑块
age = st.slider("年龄", min_value=0, max_value=100, value=25, step=1)
# 浮点滑块
price = st.slider("价格区间", min_value=0.0, max_value=1000.0, value=(100.0, 500.0))
# 数字输入框
quantity = st.number_input("采购数量", min_value=1, max_value=1000, value=10)
# 数值显示
st.metric("选中年龄", age)
st.metric("价格范围", f"¥{price[0]} ~ ¥{price[1]}")


# 下拉框、单选、多选
# 下拉单选框
category = st.selectbox(
    "产品类别",
    options=["电子产品", "服装", "食品", "家居"],
    index=0
)

# 多选框
selected_cities = st.multiselect(
    "选择城市",
    options=["北京", "上海", "广州", "深圳", "杭州"],
    default=["北京", "上海"]
)
# 单选按钮
gender = st.radio("性别", options=["男", "女", "其他"], horizontal=True)
# 复选框
show_detail = st.checkbox("显示详细数据", value=True)


# 文本型输入
# 单行文本
name = st.text_input("用户名", value="", placeholder="请输入姓名")
# 多行文本
feedback = st.text_area("用户反馈", height=150, max_chars=500)
# 密码输入
password = st.text_input("密码", type="password")


# 日期与时间
from datetime import date, datetime
# 日期选择
start_date = st.date_input("开始日期", value=date(2024, 1, 1))
date_range = st.date_input("日期范围", value=(date(2024,1,1), date(2024,1,31)))
# 时间选择
appointment_time = st.time_input("预约时间", value=datetime.now().time())
# 颜色选择器
color = st.color_picker("选择主题色", "#0066CC")


# 按钮与触发类
# 普通按钮（每次点击返回 True，触发重跑）
if st.button("生成报表"):
    st.success("报表生成中...")

# 主按钮（高亮样式）
if st.button("确认提交", type="primary"):
    st.info("已提交")
# 表单：批量提交，不实时触发
with st.form("sales_form"):
    product = st.text_input("产品名")
    amount = st.number_input("金额", min_value=0)
    submitted = st.form_submit_button("提交")
    if submitted:
        st.success(f"已录入：{product}，金额：{amount}")
# 文件上传
# pandas 默认不包含读取 .xlsx (Excel) 文件的解析引擎
# 需要额外安装 openpyxl 库，pandas 才能成功读取 Excel 文件
uploaded_file = st.file_uploader("上传销售数据 Excel", type=["xlsx", "csv"])
if uploaded_file is not None:
    import pandas as pd
    df = pd.read_excel(uploaded_file)
    st.dataframe(df)