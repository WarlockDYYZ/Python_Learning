# 使用真实数据的相关性分析示例
# 使用鸢尾花数据集演示散点图矩阵
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
import pandas as pd

# 加载数据集
iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['target'] = iris.target

# 4个特征 → 创建 4行4列 子图矩阵
n_features = 4
fig, axes = plt.subplots(n_features, n_features, figsize=(8, 7))
# 展平，方便索引
axes = axes.ravel()

# 特征列表
features = iris.feature_names
# 目标值对应的颜色：3类鸢尾花对应3种颜色
colors = ['red', 'green', 'blue']

# 双层循环遍历 行i、列j
for i in range(n_features):
    for j in range(n_features):
        # 计算要绘图的轴
        idx = i * 4 + j

        # 下三角：i > j 才画散点图
        if i > j:
            axes[idx].scatter(
                df[features[j]],  # X轴：第j个特征
                df[features[i]],  # Y轴：第i个特征
                c=df['target'].map(lambda x: colors[x]),
                alpha=0.6
            )
            # 设置坐标轴标签
            axes[idx].set_xlabel(features[j], fontsize=8)
            axes[idx].set_ylabel(features[i], fontsize=8)

        # 现在对角线和上三角还有保留，改一下
        # 对角线：i == j 不画图，只写特征名称
        # elif i == j:
        #     ax.text(0.5, 0.5, features[i],
        #             horizontalalignment='center',
        #             verticalalignment='center',
        #             fontsize=9)
        #     ax.set_xticks([])
        #     ax.set_yticks([])
        #
        # # 上三角：i < j 直接隐藏坐标轴
        # else:
        #     ax.set_xticks([])
        #     ax.set_yticks([])

        else:
            # 上三角 + 对角线：隐藏坐标轴、隐藏边框、清空刻度
            axes[idx].axis('off')

plt.tight_layout()
plt.show()
