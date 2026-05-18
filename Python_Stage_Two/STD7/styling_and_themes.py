import matplotlib.pyplot as plt
import numpy as np


# 1. 使用内置样式
plt.style.use('seaborn-v0_8-darkgrid')  # 使用seaborn样式

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'Noto Sans CJK SC']
plt.rcParams['axes.unicode_minus'] = False    # 正常显示负号
plt.rcParams['mathtext.default'] = 'regular'           # 修复 3D 负号
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
# 有时候自动排版是会报错的，注释就行了
# plt.tight_layout()
plt.show()


# 2. 创建自定义样式
# 定义样式字典
custom_style = {
    'font.family': 'SimHei',
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'axes.titleweight': 'bold',
    'axes.grid': True,
    'grid.alpha': 0.3,
    'lines.linewidth': 2,
    'scatter.marker': 'o',
    # 就是这行老是报错
    # scatter.size / scatter.sizes 全都不是合法的 rcParams 参数！
    # matplotlib 根本没有这个全局设置项，所以怎么写都会报错！
    # 'scatter.size': 100,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.dpi': 100,
    'figure.figsize': (10, 6),
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
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
ax.annotate(
    '最大值点',                # 1. 注释显示的文本内容
    xy=(3.14, 0.37),          # 2. 箭头【指向的目标坐标】(x,y)
    xytext=(4, 0.6),          # 3. 注释【文字所在位置坐标】(x,y)
    arrowprops=dict(          # 4. 箭头样式配置字典
        arrowstyle='->',      # 箭头样式：普通右向箭头
        color='red',          # 箭头颜色
        lw=2                  # 箭头线条宽度
    ),
    fontsize=10,              # 5. 注释文字字号
    bbox=dict(                # 6. 文字外围边框/背景样式
        boxstyle='round,pad=0.3', # 圆角矩形边框，内边距0.3
        facecolor='yellow',   # 背景填充色
        alpha=0.5             # 背景透明度 0~1
    )
)

# 设置标签和标题
ax.set_xlabel('X值')
ax.set_ylabel('Y值')
ax.set_title('使用自定义样式', fontsize=14, fontweight='bold')
ax.legend()
# plt.tight_layout()
plt.show()


# 3. 创建主题切换演示
# 主题1：科技感（蓝黑配色）
with plt.style.context('dark_background'):
    fig1, ax1 = plt.subplots(figsize=(7,6))
    x = np.linspace(0,10,100)
    ax1.plot(x, np.sin(x), 'cyan', lw=3, label='sin(x)')
    ax1.plot(x, np.cos(x), 'yellow', lw=3, label='cos(x)')
    ax1.set_title('Dark Theme', fontweight='bold')
    ax1.legend()
    ax1.grid(alpha=0.3)

# 学术风（黑白配色）
with plt.style.context('default'):
    fig2, ax2 = plt.subplots(figsize=(7,6))
    x = np.linspace(0,10,100)
    ax2.plot(x, np.sin(x), 'k', lw=3, label='sin(x)')
    ax2.plot(x, np.cos(x), 'gray', lw=3, label='cos(x)')
    ax2.set_title('Light Theme', fontweight='bold')
    ax2.legend()
    ax2.grid(alpha=0.3)

plt.show()
