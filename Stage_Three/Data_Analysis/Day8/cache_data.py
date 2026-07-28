import streamlit as st
import pandas as pd


@st.cache_data(ttl=3600)  # 缓存有效期 3600 秒（1小时）
def load_sales_data(file_path):
    """加载销售数据，相同路径只读取一次"""
    df = pd.read_csv(file_path)
    # 模拟耗时处理
    return df

# 第一次调用：执行函数，缓存结果
# 第二次调用：相同参数直接返回缓存
df = load_sales_data("sales.csv")
st.table(df)

# 清除缓存
if st.button("刷新数据"):
    load_sales_data.clear()  # 清除该函数的缓存
    st.rerun()               # 强制脚本立即从头重跑一次


@st.cache_resource
def get_database_connection():
    """数据库连接只创建一次，全局复用"""
    import sqlite3
    conn = sqlite3.connect("sales.db")
    return conn

conn = get_database_connection()
# 所有用户会话共享同一个连接对象