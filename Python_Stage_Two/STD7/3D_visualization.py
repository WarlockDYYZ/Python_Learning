import matplotlib.pyplot as plt
import numpy as np


# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建3D图形
fig = plt.figure(figsize=(14, 10))
# 1. 3D表面图
ax1 = fig.add_subplot(2, 2, 1, projection='3d')
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2)) / (np.sqrt(X**2 + Y**2) + 0.001)
# 使用viridis颜色映射
surf = ax1.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.8)
ax1.set_title('3D表面图', fontsize=12, fontweight='bold')
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')
# 2. 3D散点图
ax2 = fig.add_subplot(2, 2, 2, projection='3d')
# 创建螺旋线数据
theta = np.linspace(0, 8*np.pi, 1000)
r = np.linspace(0.5, 5, 1000)
x_scatter = r * np.cos(theta)
y_scatter = r * np.sin(theta)
z_scatter = np.linspace(0, 10, 1000)
# 按高度设置颜色
colors = z_scatter
# 绘制散点图
scatter = ax2.scatter(x_scatter, y_scatter, z_scatter, c=colors,
                      cmap='plasma', s=10, alpha=0.8)
ax2.set_title('3D散点图', fontsize=12, fontweight='bold')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')
# 添加颜色条
cbar = plt.colorbar(scatter, ax=ax2)
cbar.set_label('高度')
# 3. 3D线图
ax3 = fig.add_subplot(2, 2, 3, projection='3d')
# 创建 Lissajous 曲线
t = np.linspace(0, 2*np.pi, 1000)
x_line = np.sin(2*t)
y_line = np.sin(3*t)
z_line = np.sin(4*t)
# 绘制线图
ax3.plot(x_line, y_line, z_line, 'b-', linewidth=2)
ax3.set_title('3D线图', fontsize=12, fontweight='bold')
ax3.set_xlabel('X')
ax3.set_ylabel('Y')
ax3.set_zlabel('Z')
# 4. 3D柱状图
ax4 = fig.add_subplot(2, 2, 4, projection='3d')
# 创建数据
x_pos = np.arange(5)
y_pos = np.arange(4)
X_pos, Y_pos = np.meshgrid(x_pos, y_pos)
X_pos = X_pos.ravel()
Y_pos = Y_pos.ravel()
z_pos = np.zeros_like(X_pos)
# 柱状图高度
height = np.random.randint(1, 10, size=20)
dx = np.ones_like(X_pos) * 0.8
dy = np.ones_like(Y_pos) * 0.8
# 按高度设置颜色
colors_bar = plt.cm.viridis(height/height.max())
# 绘制3D柱状图
bars = ax4.bar3d(X_pos, Y_pos, z_pos, dx, dy, height, color=colors_bar, alpha=0.8)
ax4.set_title('3D柱状图', fontsize=12, fontweight='bold')
ax4.set_xlabel('X')
ax4.set_ylabel('Y')
ax4.set_zlabel('高度')
plt.tight_layout()
plt.show()