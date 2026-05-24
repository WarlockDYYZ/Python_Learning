import matplotlib.pyplot as plt
import numpy as np


x = np.linspace(0, 10, 1000)

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
# 子图1：折线图
ax1.plot(x, np.sin(x), 'r-', linewidth=2)
ax1.set_title('(a) Sine Wave', fontsize=10)
# 子图2：散点图
ax2.scatter(np.random.rand(50), np.random.rand(50),
            s=100, c=np.random.rand(50), cmap='viridis')
ax2.set_title('(b) Scatter Plot', fontsize=10)
# 子图3：柱状图
categories = ['A', 'B', 'C', 'D']
values = [10, 20, 15, 25]
ax3.bar(categories, values, color=['red', 'green', 'blue', 'purple'])
ax3.set_title('(c) Bar Chart', fontsize=10)
# 子图4：箱线图
data = [np.random.normal(0, 1, 100), np.random.normal(2, 1, 100)]
ax4.boxplot(data, labels=['Group 1', 'Group 2'])
ax4.set_title('(d) Box Plot', fontsize=10)

plt.suptitle('Multi-panel Figure Example', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
