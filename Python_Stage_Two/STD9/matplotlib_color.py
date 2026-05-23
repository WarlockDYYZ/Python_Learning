import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# 设置全局颜色方案
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['axes.prop_cycle'] = plt.cycler(
   color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
)

# 创建示例图表
fig, ax = plt.subplots(figsize=(10, 6))
x = range(5)
y = [3, 7, 5, 8, 4]
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

bars = ax.bar(x, y, color=colors)

ax.set_title('Color Best Practices', fontsize=14, fontweight='bold')

# 添加颜色说明
legend_elements = [mpatches.Patch(color=c, label=f'Color {i+1}') for i, c in enumerate(colors)]
ax.legend(handles=legend_elements, loc='upper right')

plt.show()
