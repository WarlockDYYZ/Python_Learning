import seaborn as sns
import matplotlib.pyplot as plt


# 设置全局字体为“微软雅黑”（Windows系统自带）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# 解决负号显示成方块的问题
plt.rcParams['axes.unicode_minus'] = False
# 加载数据集
tips = sns.load_dataset("tips")


# 显示所有预设调色板
sns.palplot(sns.color_palette("deep", 10))
sns.palplot(sns.color_palette("muted", 10))
sns.palplot(sns.color_palette("bright", 10))
sns.palplot(sns.color_palette("pastel", 10))
sns.palplot(sns.color_palette("dark", 10))
sns.palplot(sns.color_palette("colorblind", 10))
plt.show()


# 创建自定义调色板
custom_palette = sns.color_palette("ch:r=-.5,l=.75", 6)  # 基于颜色轮的调色板
sns.palplot(custom_palette)

# 使用RGB值创建调色板
rgb_palette = [(0.2, 0.4, 0.6), (0.8, 0.3, 0.1), (0.9, 0.9, 0.2)]
sns.palplot(rgb_palette)

# 立方体螺旋调色板
cubehelix_palette = sns.cubehelix_palette(light=0.8, n_colors=6)
sns.palplot(cubehelix_palette)

# 明确指定要一个紫色的渐变（'purple' 也可以换成具体的十六进制色号如 '#800080'）
# 亮紫 偏白 -> 紫
purple_palette = sns.light_palette("purple", n_colors=6)
sns.palplot(purple_palette)
# 深紫 偏黑 -> 紫
purple_palette = sns.dark_palette("purple", n_colors=6)
sns.palplot(purple_palette)

plt.show()
