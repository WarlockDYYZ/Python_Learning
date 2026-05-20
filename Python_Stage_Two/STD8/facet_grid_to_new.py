import seaborn as sns
import matplotlib.pyplot as plt


# 设置全局字体为“微软雅黑”（Windows系统自带）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# 解决负号显示成方块的问题
plt.rcParams['axes.unicode_minus'] = False


# 加载数据集
tips = sns.load_dataset("tips")


# 旧版 FacetGrid 映射（map） barplot ===> 新版 sns.catplot（专门处理分类数据的图形级接口）
# 新写法：一行代码搞定分面、绘图和排序
g = sns.catplot(
    data=tips,
    x="sex", y="total_bill", col="day",  # 指定 x, y 和按 day 分列
    kind="bar",                          # 指定图表类型为条形图
    order=['Male', 'Female'],            # 明确指定顺序，消除警告
    height=4, aspect=0.5                 # 设置大小和纵横比
)
plt.show()


# 旧版 FacetGrid 映射（map） kdeplot ===> 新版 sns.displot（统一的分发图接口）
ordered_days = tips.day.value_counts().index

# 新写法：直接用 displot 绘制核密度估计(KDE)，并按 day 分行
g = sns.displot(
    data=tips,
    x="total_bill",                      # 指定单变量
    row="day",                           # 按 day 分行展示
    row_order=ordered_days,              # 指定行的排列顺序
    kind="kde",                          # 指定为核密度图
    height=1.7, aspect=4                 # 设置大小和纵横比
)
plt.show()


# 旧版 FacetGrid 映射（map） scatterplot ===> 新版 sns.scatterplot(...)
pal = dict(Lunch="seagreen", Dinner=".7")

# 新写法：直接使用 scatterplot，通过 hue 参数自动完成分色和图例添加
sns.scatterplot(
    data=tips,
    x="total_bill", y="tip",
    hue="time",                          # 按 time 字段区分颜色
    palette=pal,                         # 使用自定义调色板
    s=100, alpha=0.5                     # 设置点的大小和透明度
)
plt.show()