import seaborn as sns
import matplotlib.pyplot as plt


# 设置全局字体为“微软雅黑”（Windows系统自带）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# 解决负号显示成方块的问题
plt.rcParams['axes.unicode_minus'] = False


# 加载数据集
tips = sns.load_dataset("tips")


# 直方图与核密度估计（histplot + kdeplot）
# 1. 单变量分布
plt.figure() # 强制创建第一张新画布
sns.histplot(data=tips, x="total_bill", kde=True)

# 2. 按类别分组
plt.figure() # 强制创建第二张新画布
sns.histplot(data=tips, x="total_bill", hue="smoker", kde=True)

# 3. 核密度估计图
plt.figure() # 强制创建第三张新画布
sns.kdeplot(data=tips, x="total_bill", hue="smoker", fill=True)

# 4. 经验累积分布函数
# displot 本身就会建新画布，加上 plt.figure() 会创建一个空白的画布，不会使用到，所以不写
sns.displot(data=tips, kind="ecdf", x="total_bill", hue="smoker")

# 统一弹出所有独立的窗口
plt.show()


# 箱线图与小提琴图
# 箱线图
plt.figure()
sns.boxplot(data=tips, x="day", y="total_bill", hue="smoker")

# 小提琴图（箱线图 + KDE 核密度估计）
plt.figure()
sns.violinplot(
   data=tips,
   x="day", y="total_bill",
   hue="smoker", split=True
)

# 蜂群图（展示所有数据点）
plt.figure()
sns.swarmplot(data=tips, x="day", y="total_bill", hue="smoker")
plt.show()


# 箱线图 + 蜂群图（经典且清晰）
plt.figure(figsize=(10, 6))
# 1. 先画箱线图打底，设置浅色背景
sns.boxplot(data=tips, x="day", y="total_bill",
            color="lightgray", width=0.5)
# 2. 再叠加上蜂群图，dodge=True让不同hue的点自动错开
sns.swarmplot(data=tips, x="day", y="total_bill", hue="smoker",
              size=4, dodge=True, palette=["black", "red"])

plt.title("箱线图(骨架) + 蜂群图(真实数据点)")
plt.show()

# 小提琴图 + 蜂群图（揭示复杂分布）
plt.figure(figsize=(10, 6))
# 1. 先画小提琴图展示整体密度轮廓，inner=None去掉内部默认的迷你箱线图
sns.violinplot(data=tips, x="day", y="total_bill",
               color="skyblue", inner=None)
# 2. 叠加上蜂群图，看清具体点的分布
sns.swarmplot(data=tips, x="day", y="total_bill",
              color="black", size=3, alpha=0.6)

plt.title("小提琴图(密度轮廓) + 蜂群图(底层细节)")
plt.show()


# 双变量的深度剖析
# 探究账单总额(total_bill)和小费(tip)的关系，并加上回归线
sns.jointplot(data=tips, x="total_bill", y="tip", kind="reg")
plt.show()

# 多变量的全景扫描
iris = sns.load_dataset("iris")
# 一次性看鸢尾花4个特征的两两关系，并按物种(hue)着色
sns.pairplot(data=iris, hue="species", diag_kind="kde", height=2.5)
plt.show()
