import matplotlib.pyplot as plt
import numpy as np


# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 创建雷达图（多维度健康评估）
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6),
                               subplot_kw=dict(projection='polar'))
# 健康指标
categories = ['血压', '心率', '血糖', '血脂', '体重指数', '运动频率']
N = len(categories)

# 患者1的数据
patient1_scores = [85, 70, 65, 90, 75, 60]
patient2_scores = [90, 85, 80, 75, 80, 85]
# 计算角度
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
patient1_scores += patient1_scores[:1]
patient2_scores += patient2_scores[:1]
angles += angles[:1]
# 绘制雷达图
ax1.plot(angles, patient1_scores, 'o-', linewidth=2, label='患者1', color='red')
ax1.fill(angles, patient1_scores, alpha=0.25, color='red')
ax1.set_xticks(angles[:-1])
ax1.set_xticklabels(categories)
ax1.set_ylim(0, 100)
ax1.set_title('患者健康状况雷达图', fontsize=14, fontweight='bold', pad=20)
ax1.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))

# 患者2的雷达图
ax2.plot(angles, patient2_scores, 'o-', linewidth=2, label='患者2', color='blue')
ax2.fill(angles, patient2_scores, alpha=0.25, color='blue')
ax2.set_xticks(angles[:-1])
ax2.set_xticklabels(categories)
ax2.set_ylim(0, 100)
ax2.set_title('患者健康状况雷达图', fontsize=14, fontweight='bold', pad=20)
ax2.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
plt.tight_layout()
plt.show()

# 2. 创建热图（医学指标相关性）
fig, ax = plt.subplots(figsize=(10, 8))
# 创建医学指标相关性数据
indicators = ['年龄', '血压', '心率', '血糖', '血脂', 'BMI']
correlation_matrix = np.array([
    [1.0, 0.65, 0.45, 0.35, 0.55, 0.75],
    [0.65, 1.0, 0.78, 0.82, 0.68, 0.72],
    [0.45, 0.78, 1.0, 0.65, 0.58, 0.62],
    [0.35, 0.82, 0.65, 1.0, 0.85, 0.78],
    [0.55, 0.68, 0.58, 0.85, 1.0, 0.81],
    [0.75, 0.72, 0.62, 0.78, 0.81, 1.0]
])

# 绘制热图
im = ax.imshow(correlation_matrix, cmap='RdYlGn', aspect='auto')

# 设置刻度
ax.set_xticks(np.arange(len(indicators)))
ax.set_yticks(np.arange(len(indicators)))
ax.set_xticklabels(indicators)
ax.set_yticklabels(indicators)

# 旋转刻度
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# 添加数值
for i in range(len(indicators)):
    for j in range(len(indicators)):
        text = ax.text(j, i, f'{correlation_matrix[i, j]:.2f}',
                       ha="center", va="center", color="black")

# 添加颜色条
cbar = plt.colorbar(im)
cbar.set_label('相关系数', rotation=270, labelpad=20)

# 设置标题
ax.set_title('医学指标相关性热图', fontsize=16, fontweight='bold', pad=20)

plt.tight_layout()
plt.show()