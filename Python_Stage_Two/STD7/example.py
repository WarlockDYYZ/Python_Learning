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
plt.show()
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
plt.show()


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
plt.show()


# fig & ax
# 2行1列 两个坐标轴
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

ax1.plot(x, np.sin(x))   # 在第一个坐标系画
ax2.plot(x, np.cos(x))   # 在第二个坐标系画
# 有一个 plt.show() 就会显示前面画好的所有图像
plt.show()


# 分组柱状图示例
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 创建数据
categories = ['苹果', '香蕉', '橙子', '葡萄', '西瓜']
sales_2023 = [150, 120, 80, 95, 60]
sales_2024 = [165, 135, 95, 110, 75]
# 设置位置
# [0, 1, 2, 3, 4]，代表 5 个水果在 X 轴上的中心位置
x = np.arange(len(categories))
# 每根柱子的宽度，用来让两根柱子左右分开，不重叠
width = 0.35
# 创建图表
fig, ax = plt.subplots(figsize=(10, 6))
# 绘制柱状图
# ax.bar(位置, 高度, 宽度, 标签, 颜色)
# ax.bar(第一个参数) 传入的就是柱子中心点的 x 坐标
bars1 = ax.bar(x - width/2, sales_2023, width, label='2023年', color='#1f77b4')
bars2 = ax.bar(x + width/2, sales_2024, width, label='2024年', color='#ff7f0e')
# 设置标题和标签
ax.set_title('水果销售额对比（万元）', fontsize=14, fontweight='bold')
ax.set_xlabel('水果类别', fontsize=12)
ax.set_ylabel('销售额（万元）', fontsize=12)
# 设置x轴刻度
# x 轴下的小竖线，值是上面生成的 x = [0, 1, 2, 3, 4]
ax.set_xticks(x)
# 把刻度变成 苹果、香蕉、橙子…
ax.set_xticklabels(categories)
# 添加图例
ax.legend()
# 添加数值标签
for bar in bars1:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2.,  # X 坐标：柱子中心
        height,  # Y 坐标：柱子高度
        f'{height}',  # 显示的文字
        ha='center', va='bottom'  # 居中、靠柱子顶部
    )
for bar in bars2:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height}', ha='center', va='bottom')
plt.tight_layout()
plt.show()


# 堆叠柱状图示例
# 创建堆叠数据
labels = ['A产品', 'B产品', 'C产品']
men_means = [20, 35, 30]
women_means = [25, 32, 34]
# 创建图表
fig, ax = plt.subplots(figsize=(10, 6))
# 绘制堆叠柱状图
x = np.arange(len(labels))
width = 0.35

# 第一层（男性）：直接画在底部
bars1 = ax.bar(x, men_means, width, label='男性', color='lightblue')
# bottom 参数 bottom=men_means 意思：从男性数据的顶部开始画，堆叠数据
bars2 = ax.bar(x, women_means, width, bottom=men_means, label='女性', color='pink')

# 设置标题和标签
ax.set_title('不同产品男女购买量', fontsize=14, fontweight='bold')
ax.set_xlabel('产品类型', fontsize=12)
ax.set_ylabel('购买量（件）', fontsize=12)
# 设置x轴刻度
ax.set_xticks(x)
ax.set_xticklabels(labels)
# 添加图例
ax.legend()


def autolabel(bars, bottom_vals=None):
    for i, bar in enumerate(bars):
        height = bar.get_height()

        # 计算当前段的底部位置
        if bottom_vals is not None:
            bottom = bottom_vals[i]
        else:
            bottom = 0

        # 🔥 核心：垂直居中
        y_pos = bottom + height / 2

        ax.text(
            # bar.get_x() 获取的是：柱子最左侧的 X 坐标
            # 所以，+ 柱子宽度的一半，使数值显示在柱子中间
            bar.get_x() + bar.get_width() / 2.,  # 水平居中
            y_pos,  # 垂直居中
            f'{int(height)}',
            ha='center',
            va='center'  # 文字垂直居中
        )

autolabel(bars1)
autolabel(bars2, bottom_vals=men_means)
plt.tight_layout()
plt.show()


# 饼图
# 创建数据
labels = ['Python', 'Java', 'C++', 'JavaScript', '其他']
sizes = [35, 25, 20, 15, 5]
explode = (0.1, 0, 0, 0, 0)  # 突出显示Python
# 自定义颜色
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
# 创建图表
fig, ax = plt.subplots(figsize=(10, 8))
# 绘制饼图

# sizes & labels 饼图有几块，labels 就必须有几个！数量必须完全对应！
wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                                        autopct='%1.1f%%', shadow=True, startangle=90)

# 设置标题
ax.set_title('编程语言使用占比', fontsize=16, fontweight='bold')
# 美化文字
for text in texts:
    text.set_fontsize(12)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(10)
    autotext.set_weight('bold')
plt.tight_layout()
plt.show()


# 直方图
# 创建数据
np.random.seed(42)
# 生成正态分布数据
data_normal = np.random.normal(0, 1, 1000)
# 生成均匀分布数据
data_uniform = np.random.uniform(-2, 2, 1000)
# 创建图表
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
# 绘制正态分布直方图
ax1.hist(data_normal, bins=30, alpha=0.7, color='skyblue',
        edgecolor='black', label='正态分布')
ax1.set_title('正态分布直方图', fontsize=14, fontweight='bold')
ax1.set_xlabel('值', fontsize=12)
ax1.set_ylabel('频率', fontsize=12)
# 显示 ax1 的图列
ax1.legend()
# 绘制均匀分布直方图
ax2.hist(data_uniform, bins=30, alpha=0.7, color='lightcoral',
        edgecolor='black', label='均匀分布')
ax2.set_title('均匀分布直方图', fontsize=14, fontweight='bold')
ax2.set_xlabel('值', fontsize=12)
ax2.set_ylabel('频率', fontsize=12)
ax2.legend()
plt.tight_layout()
plt.show()

# 双变量直方图示例
# 创建二维直方图
fig, ax = plt.subplots(figsize=(10, 8))
# 生成二维正态分布数据
x = np.random.normal(0, 1, 1000)
y = np.random.normal(0, 1, 1000)
# 绘制二维直方图
hist = ax.hist2d(x, y, bins=30, cmap='Blues', density=True)
# 设置标题和标签
ax.set_title('二维直方图', fontsize=16, fontweight='bold')
ax.set_xlabel('X值', fontsize=12)
ax.set_ylabel('Y值', fontsize=12)
# 添加颜色条
cbar = plt.colorbar(hist[3], ax=ax)
print(hist[0])
cbar.set_label('密度', fontsize=10)
plt.tight_layout()
plt.show()


# 散点图
# 创建数据
np.random.seed(42)
N = 100
x = np.random.rand(N)
y = np.random.rand(N)
colors = np.random.rand(N)  # 颜色
sizes = 1000 * np.random.rand(N)  # 大小
# 创建图表
fig, ax = plt.subplots(figsize=(10, 8))
# 绘制散点图
scatter = ax.scatter(x, y, s=sizes, c=colors, cmap='viridis',
                    alpha=0.7, edgecolors='black', linewidth=1)
# 设置标题和标签
ax.set_title('散点图示例', fontsize=16, fontweight='bold')
ax.set_xlabel('X值', fontsize=12)
ax.set_ylabel('Y值', fontsize=12)
# 添加颜色条
cbar = plt.colorbar(scatter)
cbar.set_label('颜色映射值', fontsize=10)
# 设置坐标轴范围
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
# 添加网格
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
