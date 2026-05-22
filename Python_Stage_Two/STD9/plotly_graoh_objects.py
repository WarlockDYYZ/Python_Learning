import plotly.graph_objects as go
import numpy as np


# 创建3D表面图
x = np.linspace(-2, 2, 100)
y = np.linspace(-2, 2, 100)
x, y = np.meshgrid(x, y)
z = np.sin(np.sqrt(x**2 + y**2))

fig = go.Figure(
    data=[go.Surface(x=x, y=y, z=z, colorscale='viridis')]
)

fig.update_layout(
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    ),
    title='3D Surface: z = sin(√(x²+y²))'
)

# 相机控制
fig.update_layout(
    scene_camera=dict(
        eye=dict(x=1.5, y=1.5, z=1)  # 设置相机位置
    )
)

fig.show()
