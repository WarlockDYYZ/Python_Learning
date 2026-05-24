import plotly.graph_objects as go
import numpy as np


# 创建带有标注的图表
x = np.linspace(0, 10, 100)
y = np.sin(x) * np.exp(-0.1 * x)

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Signal'))

# 添加峰值标注
peak_index = np.argmax(y)
fig.add_annotation(
    x=x[peak_index], y=y[peak_index],
    text=f'Peak: {y[peak_index]:.2f}',
    showarrow=True,  # 显示箭头
    arrowhead=2,  # 箭头样式（2号风格）
    ax=0, ay=-20
)

fig.update_layout(
    title='Signal with Annotation',
    xaxis_title='Time',
    yaxis_title='Amplitude',
    # 默认图例显示是关闭的，所以即使在绘图时设置了 name='Signal' 也不会显示图例，需要手动开启，显示的位置是绘图区域的右上角
    showlegend=True
)

fig.show()
