import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches


# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 换成 Windows 必有的字体
plt.rcParams['axes.unicode_minus'] = False             # 修复负号
plt.rcParams['mathtext.default'] = 'regular'           # 修复 3D 负号

# 1. 使用内置样式
plt.style.use('seaborn-v0_8-darkgrid')  # 使用seaborn样式
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
# 绘制不同类型的图表
x = np.linspace(0, 10, 100)
ax1.plot(x, np.sin(x), 'b-', linewidth=2, label='sin(x)')
ax1.plot(x, np.cos(x), 'r--', linewidth=2, label='cos(x)')
ax1.set_title('使用seaborn样式', fontsize=14, fontweight='bold')
ax1.legend()
ax2.scatter(np.random.rand(100), np.random.rand(100),
            s=200, c=np.random.rand(100), cmap='viridis', alpha=0.7)
ax2.set_title('散点图', fontsize=14, fontweight='bold')
ax3.hist(np.random.normal(0, 1, 1000), bins=30, alpha=0.7, color='steelblue')
ax3.set_title('直方图', fontsize=14, fontweight='bold')
ax4.bar(['A', 'B', 'C', 'D', 'E'], [12, 18, 25, 15, 20],
        color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
ax4.set_title('柱状图', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
# 2. 创建自定义样式
# 定义样式字典
custom_style = {
    'font.family': 'DejaVu Sans',
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'axes.grid': True,
    'grid.alpha': 0.3,
    'lines.linewidth': 2,
    'scatter.marker': 'o',
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.dpi': 100,
    'figure.figsize': (10, 6),
    'savefig.dpi': 300,
    # ❌ 删掉这行：你的版本不支持 savefig.bbox_inches
}
# 使用自定义样式
plt.rcParams.update(custom_style)
# 创建图表
fig, ax = plt.subplots()
# 绘制示例数据
x = np.linspace(0, 10, 100)
y = np.sin(x) * np.exp(-0.1 * x)
# 绘制主曲线
ax.plot(x, y, 'b-', label='衰减正弦波')
# 添加填充区域
ax.fill_between(x, y, 0, where=(y > 0), alpha=0.3, color='green')
ax.fill_between(x, y, 0, where=(y < 0), alpha=0.3, color='red')
# 添加标注
ax.annotate('最大值点', xy=(3.14, 0.37), xytext=(4, 0.6),
            arrowprops=dict(arrowstyle='->', color='red', lw=2),
            fontsize=10,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.5))
# 设置标签和标题
ax.set_xlabel('X值')
ax.set_ylabel('Y值')
ax.set_title('使用自定义样式', fontsize=14, fontweight='bold')
ax.legend()
plt.tight_layout()
plt.show()
# 3. 创建主题切换演示
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
# 主题1：科技感（蓝黑配色）
with plt.style.context(['dark_background']):
    ax1.plot(np.linspace(0, 10, 100), np.sin(np.linspace(0, 10, 100)),
             'cyan', linewidth=3, label='sin(x)')
    ax1.plot(np.linspace(0, 10, 100), np.cos(np.linspace(0, 10, 100)),
             'yellow', linewidth=3, label='cos(x)')
    ax1.set_title('暗背景主题', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
# 主题2：学术风（黑白配色）
with plt.style.context(['default']):
    ax2.plot(np.linspace(0, 10, 100), np.sin(np.linspace(0, 10, 100)),
             'black', linewidth=3, label='sin(x)')
    ax2.plot(np.linspace(0, 10, 100), np.cos(np.linspace(0, 10, 100)),
             'gray', linewidth=3, label='cos(x)')
    ax2.set_title('学术风格', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()