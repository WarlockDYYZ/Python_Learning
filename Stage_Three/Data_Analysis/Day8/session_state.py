import streamlit as st


# session_state 基础操作
# 1. 初始化
if "counter" not in st.session_state:
    st.session_state.counter = 0

# 2. 显示
st.write(f"当前计数：{st.session_state.counter}")

# 3. 定义回调函数
def add_one():
    st.session_state.counter += 1

def reset_counter():
    st.session_state.counter = 0

# 4. 绑定回调函数
st.button("+1", on_click=add_one)
st.button("重置", on_click=reset_counter)

# 删除
if st.button("删除计数器"):
    del st.session_state.counter


# 输入组件可以通过 key 参数直接绑定到 session_state，无需手动赋值
# 1. 初始化状态（防止首次运行报错）
if "username" not in st.session_state:
    st.session_state.username = "访客"

# 2. 定义回调函数：在脚本重跑前修改状态
def fill_default_name():
    st.session_state.username = "张三"

# 3. 渲染输入框（自动绑定 session_state.username）
st.text_input("用户名", key="username")

# 4. 渲染按钮，通过 on_click 绑定回调
st.button("填入默认值", on_click=fill_default_name)

# 5. 显示结果
st.write(f"你好，{st.session_state.username}")


# 组件值变化时触发回调函数，用于复杂状态联动
def update_total():
    st.session_state.total = (
        st.session_state.price * st.session_state.quantity
    )

st.number_input("单价", key="price", value=100, on_change=update_total)
st.number_input("数量", key="quantity", value=1, on_change=update_total)

st.metric("总价", st.session_state.get("total", 100))