import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np


x = np.linspace(0, 10, 1000)
y = np.sin(x) * np.exp(-0.1 * x)

fig = plt.figure(figsize=(12, 10))
# 创建复杂的GridSpec布局
gs = gridspec.GridSpec(3, 3, height_ratios=[2, 1, 1], width_ratios=[1, 1, 0.5])

# 主图占据前两行和前两列
ax_main = plt.subplot(gs[0:2, 0:2])
ax_main.plot(x, y, 'b-', linewidth=2)
ax_main.set_title('Main Plot', fontsize=12)

# 子图1
ax1 = plt.subplot(gs[0, 2])
ax1.hist(np.random.normal(0, 1, 1000), bins=30, color='red', alpha=0.7)
ax1.set_title('Hist', fontsize=9)
# 子图2
ax2 = plt.subplot(gs[1, 2])
ax2.plot(x, np.cos(x), 'g-', linewidth=1)
ax2.set_title('Cos', fontsize=9)
# 子图3
ax3 = plt.subplot(gs[2, :2])
categories = ['X', 'Y', 'Z']
values = [35, 25, 40]
ax3.pie(values, labels=categories, autopct='%1.1f%%')
ax3.set_title('Pie Chart', fontsize=9)

plt.suptitle('Complex Grid Layout Example', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
