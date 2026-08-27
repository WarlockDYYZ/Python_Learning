import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


# 假设已有漏斗数据
funnel_data = {
    '阶段': ['访问首页', '浏览商品', '加入购物车', '开始结算', '完成支付'],
    '用户数': [1000, 800, 500, 300, 100],
    '转化率': [100.0, 80.0, 62.5, 60.0, 33.3]
}

# 创建DataFrame
df = pd.DataFrame(funnel_data)

# 横向漏斗图
st.title('用户行为漏斗分析')

# 创建Matplotlib图表
fig, ax = plt.subplots(figsize=(10, 6))

# 生成同色系渐变色（这里使用 Blues 色系，从深蓝到浅蓝）
cmap = cm.get_cmap('Blues')
colors = [cmap(0.9 - i * 0.15) for i in range(len(df))]

# 绘制横向柱状图
bars = ax.barh(y=df['阶段'], width=df['用户数'], color=colors)

# 从上到下显示（反转 Y 轴）
ax.invert_yaxis()

# 添加转化率标签
for i, (user_count, conversion_rate) in enumerate(zip(df['用户数'], df['转化率'])):
    ax.text(user_count + 15, i, f"{conversion_rate:.1f}%", va='center', fontsize=12, color='#333333')

# 设置标题和坐标轴标签
ax.set_title('用户行为漏斗分析', fontsize=14)
ax.set_xlabel('用户数', fontsize=12)
ax.set_ylabel('')

# 调整图表样式：去除边框，添加 X 轴网格
for spine in ['top', 'right', 'bottom', 'left']:
    ax.spines[spine].set_visible(False)
ax.grid(axis='x', linestyle='--', linewidth=0.5, alpha=0.7)

# 显示图表
st.pyplot(fig)

# 补充说明
st.write('**漏斗分析说明**')
st.write('1. 漏斗图展示用户从访问首页到完成支付的完整行为路径')
st.write('2. 横向柱状图表示各阶段用户数量')
st.write('3. 百分比标签表示当前阶段与前一阶段的转化率')
st.write('4. 漏斗底部用户数越少，表示流失率越高')