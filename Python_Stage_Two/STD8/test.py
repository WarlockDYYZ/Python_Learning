import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# 设置Seaborn默认样式
sns.set_theme()

# 加载示例数据集（Seaborn内置数据集）
tips = sns.load_dataset("tips")

# 绘制基础图表
sns.relplot(data=tips, x="total_bill", y="tip", hue="day")
plt.show()