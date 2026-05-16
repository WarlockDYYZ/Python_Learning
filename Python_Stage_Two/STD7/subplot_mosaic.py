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
# x_pos = np.arange(5)      # [0,1,2,3,4] 柱子横向排列位置
# y_pos = np.zeros(5)       # [0,0,0,0,0] 全部固定在y=0这条线上
# z_pos = np.zeros(5)       # [0,0,0,0,0] 柱子从地面z=0开始往上长
# dx = np.ones(5)   # 每根柱子宽度 = 1
# dy = np.ones(5)   # 每根柱子厚度 = 1
# dz = [12, 18, 25, 15, 20]
# ax4.bar3d(x_pos, y_pos, z_pos, dx, dy, dz, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
# ax4.set_title('3D柱状图', fontsize=10)
# 1. 生成5*5网格坐标
x_pos, y_pos = np.meshgrid(np.arange(5), np.arange(5))
# 展平成一维数组
x_pos = x_pos.flatten()
y_pos = y_pos.flatten()

# 所有柱子都从z=0地面开始
z_pos = np.zeros_like(x_pos)

# 单根底面尺寸 1*1
dx = np.ones_like(x_pos)
dy = np.ones_like(x_pos)

# 高度：0~25 随机
dz = np.random.uniform(0, 25, size=x_pos.shape)

# 绘图
ax4.bar3d(x_pos, y_pos, z_pos,
        dx, dy, dz,
        color='skyblue',   # 颜色
        alpha=0.7)         # 透明度（0-1）
        # 根据高度自动变色（最好看）
        # color=plt.cm.viridis(dz/25), alpha=0.8
        # 每根柱子随机颜色
        # color=np.random.rand(len(x_pos),3), alpha=0.7
        # 半透明玻璃感（推荐）
        # color='teal', alpha=0.5
        # 高度越高颜色越暖
        # color=plt.cm.coolwarm(dz/25)
# )
ax4.set_title('5×5排布 | 单根1×1底面 | 随机高度0-25', fontsize=10)


plt.tight_layout()
plt.show()