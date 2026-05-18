import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap


# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


# 1. 创建自定义颜色映射
# 定义颜色节点（从蓝到绿到红）
colors = [(0, 0, 1), (0, 1, 0), (1, 0, 0)]  # 蓝、绿、红
n_bins = 256  # 颜色数量

# 创建颜色映射
cmap_custom = LinearSegmentedColormap.from_list('custom_map', colors, N=n_bins)


# 2. 创建数据
x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y)


# 3. 创建图表
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
# 使用自定义颜色映射
im1 = ax1.imshow(Z, cmap=cmap_custom, extent=[-3, 3, -3, 3])
ax1.set_title('自定义颜色映射', fontsize=14, fontweight='bold')
ax1.set_xlabel('X')
ax1.set_ylabel('Y')

# 添加颜色条
cbar1 = plt.colorbar(im1, ax=ax1)
cbar1.set_label('Z值')

# 使用内置颜色映射对比
im2 = ax2.imshow(Z, cmap='RdBu', extent=[-3, 3, -3, 3])
ax2.set_title('内置RdBu颜色映射', fontsize=14, fontweight='bold')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')

# 添加颜色条
cbar2 = plt.colorbar(im2, ax=ax2)
cbar2.set_label('Z值')

plt.tight_layout()
plt.show()


# 4. 创建颜色映射对比图
fig, ax = plt.subplots(figsize=(12, 2))

# 展示所有内置颜色映射
cmaps = ['viridis', 'plasma', 'inferno', 'magma', 'cividis',
         'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
         'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
         'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn',
         'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
         'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
         'hot', 'afmhot', 'gist_heat', 'copper',
         'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
         'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']

# 绘制颜色映射条 —— 修复版
pos = 0
bar_width = 1       # 每个色条宽度
for i, cmap in enumerate(cmaps):
    # 关键修复：生成 0~1 的渐变数据，才能显示色图渐变
    gradient_data = np.linspace(0, 1, 100).reshape(-1, 1)
    ax.imshow(gradient_data, cmap=cmap, aspect='auto', extent=[pos, pos + bar_width, 0, 1])
    pos += bar_width

ax.set_xlim(0, pos)
ax.set_xticks([])
ax.set_yticks([])
ax.set_title('所有内置颜色映射', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.show()
