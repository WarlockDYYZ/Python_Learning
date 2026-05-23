import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 创建数据
correlation_matrix = np.corrcoef(np.random.randn(10, 5))
print(np.random.randn(10, 5))
print(correlation_matrix)

# 绘图配置
sns.set_theme(style="white")
plt.figure(figsize=(10, 8))

# 创建相关系数热力图
ax = sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="RdBu",
    vmin=-1, vmax=1
)

plt.title('相关性矩阵热图(Correlation Matrix Heatmap)', fontsize=16, fontweight='bold')
plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

plt.show()
