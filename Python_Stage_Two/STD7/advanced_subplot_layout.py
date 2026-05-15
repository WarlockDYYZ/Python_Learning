import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建Figure和GridSpec
# 创建一张 16 * 12 的画布
fig = plt.figure(figsize=(16, 12))
# 创建复杂的GridSpec布局
gs = fig.add_gridspec(3, 3, height_ratios=[2, 1, 1],
                      width_ratios=[1, 1, 0.2],
                      hspace=0.3, wspace=0.3)

# 主图（占据2行2列）
ax1 = fig.add_subplot(gs[0:2, 0:2])
x = np.linspace(0, 10, 1000)
ax1.plot(x, np.sin(x) * np.cos(x), 'b-', linewidth=2)
ax1.set_title('主图', fontsize=14, fontweight='bold')

# 子图2
ax2 = fig.add_subplot(gs[0, 2])
ax2.hist(np.random.normal(0, 1, 1000), bins=30, color='red', alpha=0.7)
ax2.set_title('直方图', fontsize=10)

# 子图3
ax3 = fig.add_subplot(gs[1, 2])
ax3.scatter(np.random.rand(50), np.random.rand(50), s=100, c='green')
ax3.set_title('散点图', fontsize=10)

# 子图4（占据第2行整行）
ax4 = fig.add_subplot(gs[2, :])
categories = ['A', 'B', 'C', 'D', 'E']
values = [12, 18, 25, 15, 20]
ax4.bar(categories, values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
ax4.set_title('水平柱状图', fontsize=14, fontweight='bold')

plt.show()