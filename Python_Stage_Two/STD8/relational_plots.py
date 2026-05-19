import seaborn as sns
import matplotlib.pyplot as plt


# 加载数据集
tips = sns.load_dataset("tips")

# 基础散点图（scatterplot）
sns.scatterplot(data=tips, x="total_bill", y="tip")
# 按类别着色（hue语义）
sns.scatterplot(data=tips, x="total_bill", y="tip", hue="smoker")
# 同时使用颜色和样式语义
sns.scatterplot(
    data=tips,
    x="total_bill", y="tip",
    hue="smoker", style="smoker"
)
# 使用数值型hue（按大小渐变）
sns.scatterplot(data=tips, x="total_bill", y="tip", hue="size")
plt.show()


# 折线图（lineplot）
# 加载示例数据
fmri = sns.load_dataset("fmri")
# 基础折线图
sns.lineplot(data=fmri, x="timepoint", y="signal")
# 按事件分组
sns.lineplot(data=fmri, x="timepoint", y="signal", hue="event")
# 显示置信区间（默认95%）
sns.lineplot(data=fmri, x="timepoint", y="signal", hue="region")
# 关闭聚合和置信区间
sns.lineplot(
    data=fmri,
    x="timepoint", y="signal",
    estimator=None, errorbar=None
)
plt.show()


# 子图
# 创建分面子图
sns.relplot(
    data=tips,
    x="total_bill", y="tip", hue="smoker",
    col="time", style="smoker"
)
# 更复杂的分面布局
sns.relplot(
    data=fmri, kind="line",
    x="timepoint", y="signal", hue="subject",
    col="region", row="event", height=3
)
plt.show()