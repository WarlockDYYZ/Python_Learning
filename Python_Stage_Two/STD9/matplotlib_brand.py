import matplotlib.pyplot as plt


# 设置品牌颜色
brand_colors = {
    'primary': '#1f77b4',  # 主色调
    'secondary': '#ff7f0e',  # 辅助色调
    'accent': '#2ca02c',     # 强调色
    'background': '#f8f9fa', # 背景色
    'text': '#212529'        # 文本颜色
}

# 创建品牌风格的图表
fig, ax = plt.subplots(figsize=(10, 6))
# 绘制品牌颜色示例
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
bars = ax.bar(range(5), [10, 20, 15, 25, 20], color=colors)
# 设置品牌样式
ax.set_facecolor(brand_colors['background'])
ax.set_title('Brand Colors Example', fontsize=16, fontweight='bold',
             color=brand_colors['text'])
ax.set_xlabel('Category', fontsize=12, color=brand_colors['text'])
ax.set_ylabel('Value', fontsize=12, color=brand_colors['text'])
ax.tick_params(axis='x', colors=brand_colors['text'])
ax.tick_params(axis='y', colors=brand_colors['text'])
ax.grid(True, alpha=0.3, color='gray')

plt.tight_layout()
plt.show()
