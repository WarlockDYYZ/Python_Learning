import streamlit as st


# 标题层级
st.title("一级大标题")      # 页面主标题
st.header("二级标题")       # 章节标题
st.subheader("三级标题")    # 小节标题

# 普通文本
st.text("纯文本，等宽字体")
st.write("万能输出：可显示文本、DataFrame、图表等")
st.markdown("### Markdown 语法\n- 支持 **加粗**\n- 支持 [链接](https://streamlit.io)")
st.caption("小字说明文字，常用于注释")
st.latex(r"\sum_{i=1}^{n} x_i = S")  # LaTeX 公式

# 强调容器
st.success("✅ 成功提示")
st.info("ℹ️ 信息提示")
st.warning("⚠️ 警告提示")
st.error("❌ 错误提示")
st.exception(ValueError("示例异常"))


# 水平分割线
st.divider()
# 进度条
import time
progress_bar = st.progress(0)
for i in range(100):
    time.sleep(0.01)
    progress_bar.progress(i + 1)

# 状态徽标
st.metric(label="本月销售额", value="¥128,500", delta="+12.5%")