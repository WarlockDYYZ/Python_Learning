import matplotlib.pyplot as plt
import numpy as np


# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建马赛克布局
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 8),
                                             subplot_kw=dict(projection='3d'))
# 3D表面图
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))
ax1.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
ax1.set_title('3D表面图', fontsize=10)

# 3D散点图
ax2.scatter(np.random.rand(100), np.random.rand(100), np.random.rand(100),
            c=np.random.rand(100), cmap='plasma', s=100)
ax2.set_title('3D散点图', fontsize=10)
# 3D线图
ax3.plot(np.linspace(0, 10, 100), np.sin(np.linspace(0, 10, 100)),
         np.cos(np.linspace(0, 10, 100)), 'b-', linewidth=2)
ax3.set_title('3D线图', fontsize=10)
# 3D柱状图
x_pos = np.arange(5)
y_pos = np.zeros(5)
z_pos = np.zeros(5)
dx = np.ones(5)
dy = np.ones(5)
dz = [12, 18, 25, 15, 20]
ax4.bar3d(x_pos, y_pos, z_pos, dx, dy, dz, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
ax4.set_title('3D柱状图', fontsize=10)
plt.tight_layout()
plt.show()