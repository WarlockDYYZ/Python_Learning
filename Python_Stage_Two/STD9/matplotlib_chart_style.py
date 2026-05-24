import matplotlib.pyplot as plt
import numpy as np


# 设置科研图表样式
plt.rcParams.update({
    'font.size': 8,  # 全局字体大小
    'axes.labelsize': 10,  # 轴标签字体大小
    'axes.titlesize': 12,  # 标题字体大小
    'xtick.labelsize': 8,  # x轴刻度标签字体大小
    'ytick.labelsize': 8,  # y轴刻度标签字体大小
    'legend.fontsize': 8,  # 图例字体大小
    'figure.dpi': 300,  # 设置高分辨率
    'savefig.dpi': 600,  # 保存高分辨率图片
    'font.family': 'serif',  # 使用衬线字体
    # 'text.usetex': True,  # 使用LaTeX渲染文本
})

# 创建科研风格的图表
fig, ax = plt.subplots(figsize=(6, 4))  # 标准期刊双栏宽度

# 生成数据
x = np.linspace(0, 10, 1000)
y = np.sin(x) * np.exp(-0.1 * x)

# 绘制主曲线
ax.plot(x, y, 'b-', linewidth=1.5, label='$sin(x)e^{-0.1x}$')

# 添加误差带
y_error = 0.1 * np.abs(y)
ax.fill_between(x, y - y_error, y + y_error, alpha=0.2, color='blue')

# 设置标签和标题
ax.set_xlabel('$x$', fontsize=10)
ax.set_ylabel('$f(x)$', fontsize=10)
ax.set_title('Damped Sine Wave', fontsize=12, fontweight='bold')

# 添加图例
ax.legend(loc='upper right')

# 调整布局
plt.tight_layout()

# 保存为EPS文件
plt.savefig('damped_sine.eps', format='eps', bbox_inches='tight')
plt.show()
