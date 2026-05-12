import matplotlib.pyplot as plt
import matplotlib
import numpy as np


# 验证安装
print(f"Matplotlib版本: {matplotlib.__version__}")


# 配置中文字体支持
# 方法1：全局配置（推荐）
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']  # 设置英文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
# 其实，后一次赋值会直接覆盖前一次，所以实际上只有 SimHei（黑体）生效了。
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

# 方法2：使用FontProperties（局部设置）
from matplotlib.font_manager import FontProperties
font = FontProperties(fname='/path/to/your/font.ttf', size=12)

# 方法3：在代码中动态设置
plt.rcParams.update({
   'font.family': 'sans-serif',
   'font.sans-serif': ['SimHei', 'Arial Unicode MS', 'DejaVu Sans'],
   'axes.unicode_minus': False
})


# 面向对象风格
# 创建Figure和Axes
fig, ax = plt.subplots(figsize=(10, 6))
# 绘制数据
x = np.linspace(0, 10, 100)
y = np.sin(x)
ax.plot(x, y, 'b-', linewidth=2, label='sin(x)')
# 设置标签和标题
ax.set_xlabel('X轴', fontsize=12)
ax.set_ylabel('Y轴', fontsize=12)
ax.set_title('正弦曲线', fontsize=14, fontweight='bold')
# 添加图例
ax.legend()
# 添加网格
ax.grid(True, alpha=0.3)
# 显示图表
# plt.show()
# 保存图表
fig.savefig('sine_curve.png', dpi=300, bbox_inches='tight')


# pyplot 过程式风格
plt.figure(figsize=(10, 6))
x = np.linspace(0, 10, 100)
plt.plot(x, np.cos(x), 'b-', linewidth=2, label="cos(x)")
plt.xlabel('X轴')
plt.ylabel('Y轴')
plt.title('余弦曲线')
# 单独一个文件的话按下面那一行写是可以，但是
plt.legend()
plt.grid(True)
# plt.show()


# Line Plot
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 创建数据
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.tan(x)
# 创建图表
fig, ax = plt.subplots(figsize=(12, 8))
# 绘制多条曲线

# 见名知意，linewidth 线宽， marker 标记， markersize标记大小
ax.plot(x, y1, 'b-', linewidth=2, marker='o', markersize=6, label='正弦函数')
ax.plot(x, y2, 'r--', linewidth=2, marker='s', markersize=6, label='余弦函数')
ax.plot(x, y3, 'g-.', linewidth=2, marker='^', markersize=6, label='正切函数')
# 设置标题和标签
ax.set_title('三角函数曲线对比', fontsize=16, fontweight='bold')
ax.set_xlabel('X值', fontsize=12)
ax.set_ylabel('Y值', fontsize=12)
# 设置坐标轴范围
ax.set_xlim(-0.5, 10.5)  # 左 右
ax.set_ylim(-1.5, 1.5)    # 下 上
# 添加图例
ax.legend(loc='upper right')
# 添加网格
ax.grid(True, alpha=0.3)
# 添加水平参考线
# 因为设置 y = 0，所以这条线与 x 轴重合
ax.axhline(y=0, color='purple', linestyle='-', linewidth=1)
plt.tight_layout()
# plt.show()


# fig & ax
# 2行1列 两个坐标轴
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

ax1.plot(x, np.sin(x))   # 在第一个坐标系画
ax2.plot(x, np.cos(x))   # 在第二个坐标系画
plt.show()