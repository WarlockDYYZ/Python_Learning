import plotly.graph_objects as go
import pandas as pd
import numpy as np

# 模拟健康数据
days = pd.date_range('2024-01-01', periods=30)
data = {
    'Date': days,
    'Steps': np.random.normal(8000, 1500, 30).astype(int),
    'Calories': np.random.normal(2200, 300, 30).astype(int),
    'Sleep': np.random.normal(7.5, 1, 30),
    'Weight': 75 + np.random.normal(0, 0.5, 30)
}
df = pd.DataFrame(data)

# 创建综合健康仪表板
fig = go.Figure()

# 添加步数趋势 (y1 左轴)
fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df['Steps'],
    name='Daily Steps',
    line=dict(color='#1f77b4', width=2),
    marker=dict(size=8, color='#ff7f0e', opacity=0.7)
))

# 添加卡路里趋势 (y2 右轴)
fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df['Calories'],
    name='Daily Calories',
    yaxis='y2',
    line=dict(color='#2ca02c', width=2),
    marker=dict(size=8, color='#d62728', opacity=0.7)
))

# 添加睡眠时长 (y3 左轴)
fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df['Sleep'],
    name='Sleep Hours',
    yaxis='y3',
    line=dict(color='#9467bd', width=2),
    marker=dict(size=8, color='#8c564b', opacity=0.7)
))

# 添加体重 (y4 右轴)
fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df['Weight'],
    name='Weight (kg)',
    yaxis='y4',
    line=dict(color='#e377c2', width=2),
    marker=dict(size=8, color='#7f7f7f', opacity=0.7)
))

fig.update_layout(
    title='Personal Health Tracker',
    xaxis_title='Date',

    # 第一根Y轴 (左侧)
    yaxis=dict(
        title="Steps",
        side="left"
    ),

    # 第二根Y轴 (右侧)
    yaxis2=dict(
        title="Calories",
        anchor="x",
        overlaying="y",
        side="right"
    ),

    # 第三根Y轴 (左侧，偏移)
    yaxis3=dict(
        title="Sleep (hours)",
        anchor="x",
        overlaying="y",
        side="left",
        position=0.05
    ),

    # 第四根Y轴 (右侧，偏移)
    yaxis4=dict(
        title="Weight (kg)",
        anchor="x",
        overlaying="y",
        side="right",
        position=0.95
    ),

    legend=dict(x=0, y=1.1, orientation='h'),
    height=600,
    margin=dict(l=80, r=80, t=80, b=80)
)

# 添加目标线
fig.add_hline(y=10000, line_dash='dash', line_color='red', annotation_text='10,000 Steps Goal')
fig.add_hline(y=2000, line_dash='dash', line_color='orange', annotation_text='2,000 Calories Goal')
fig.add_hline(y=8, line_dash='dash', line_color='green', annotation_text='8 Hours Sleep Goal')

fig.show()
