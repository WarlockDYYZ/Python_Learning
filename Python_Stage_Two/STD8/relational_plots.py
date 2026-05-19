import seaborn as sns
import matplotlib.pyplot as plt


# 设置全局字体为“微软雅黑”（Windows系统自带）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# 解决负号显示成方块的问题
plt.rcParams['axes.unicode_minus'] = False


# 散点图（scatterplot）
# 加载数据集
tips = sns.load_dataset("tips")
# print(tips)  # 列名为 total_bill   tip     sex smoker   day    time  size

# 基础散点图
sns.scatterplot(data=tips, x="total_bill", y="tip")
plt.show()

# 按类别着色（hue语义）
sns.scatterplot(data=tips, x="total_bill", y="tip", hue="smoker")
plt.show()

# 同时使用颜色和样式语义
sns.scatterplot(
   data=tips,
   x="total_bill", y="tip",
   hue="smoker", style="smoker"
)
plt.show()

# 使用数值型 hue（按大小渐变），点的大小根据 total_bill 变化
sns.scatterplot(data=tips, x="total_bill", y="tip", hue="size", size="total_bill")
plt.show()

# 常用参数综合示例
sns.scatterplot(
    data=tips,
    x="total_bill",   # 维度1：X轴 - 账单总额
    y="tip",          # 维度2：Y轴 - 小费金额
    hue="day",        # 维度3：颜色 - 星期几（分类变量，自动分配颜色）
    size="size",      # 维度4：大小 - 用餐人数（数值越大点越大）
    style="smoker",   # 维度5：形状 - 是否吸烟（自动区分圆圈或叉号）
    alpha=0.7,        # 增加一点透明度，防止点重叠看不清
    palette="deep"    # 换一套更好看的配色方案
    , legend=False  # 加上这一行，所有的图例都会消失
)
# 添加图标题
plt.title("餐厅小费的多维度分析")
plt.show()


# 折线图（lineplot）
# 加载示例数据
fmri = sns.load_dataset("fmri")
print(fmri)

# 基础折线图
sns.lineplot(data=fmri, x="timepoint", y="signal")
plt.show()

# 按事件分组
sns.lineplot(data=fmri, x="timepoint", y="signal", hue="event")
plt.show()

# 显示置信区间（默认95%）
sns.lineplot(data=fmri, x="timepoint", y="signal", hue="region", errorbar=('sd', 1))
plt.show()

# 关闭聚合和置信区间
# 先按受试者和时间点排好序
# fmri_sorted = fmri.sort_values(by=["subject", "timepoint"])
sns.lineplot(
    data=fmri,
    x="timepoint", y="signal",
    hue="subject",
    errorbar=None,
    legend={'loc': 'upper right'}
)
plt.show()


# relplot () 高级应用，创建多子图
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
