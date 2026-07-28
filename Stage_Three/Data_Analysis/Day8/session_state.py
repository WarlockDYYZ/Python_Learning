import streamlit as st


# session_state 基础操作
# 初始化（只在首次运行时执行）
if "counter" not in st.session_state:
    st.session_state.counter = 0

# 读取
st.write(f"当前计数：{st.session_state.counter}")

# 修改
if st.button("+1"):
    st.session_state.counter += 1
if st.button("重置"):
    st.session_state.counter = 0

# 删除
if st.button("删除计数器"):
    del st.session_state.counter


# 输入组件可以通过 key 参数直接绑定到 session_state，无需手动赋值
# 组件值自动同步到 session_state.username
st.text_input("用户名", key="username")

# 直接读取，不需要变量接收
st.write(f"你好，{st.session_state.get('username', '访客')}")

# 也可以通过修改 session_state 控制组件值
if st.button("填入默认值"):
    st.session_state.username = "张三"  # 输入框会自动更新


# 组件值变化时触发回调函数，用于复杂状态联动
def update_total():
    st.session_state.total = (
        st.session_state.price * st.session_state.quantity
    )

st.number_input("单价", key="price", value=100, on_change=update_total)
st.number_input("数量", key="quantity", value=1, on_change=update_total)

st.metric("总价", st.session_state.get("total", 100))