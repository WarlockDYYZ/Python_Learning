import seaborn as sns
import matplotlib.pyplot as plt


# 设置全局字体为“微软雅黑”（Windows系统自带）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# 解决负号显示成方块的问题
plt.rcParams['axes.unicode_minus'] = False
# 加载数据集
tips = sns.load_dataset("tips")


# 1. 设置整体画布大小 (宽,高) 单位英寸
plt.figure(figsize=(10.8, 5))

# 第一张
plt.subplot(1,2,1)
sns.regplot(data=tips, x="total_bill", y="tip")

# 第二张（多项式）
plt.subplot(1,2,2)
sns.regplot(data=tips,x="total_bill",y="tip",order=2)
# plt.show()

# lmplot 必须单独画
sns.lmplot(data=tips,x="total_bill",y="tip",col="time",hue="smoker")
plt.show()