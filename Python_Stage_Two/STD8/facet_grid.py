import seaborn as sns
import matplotlib.pyplot as plt


# 设置全局字体为“微软雅黑”（Windows系统自带）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# 解决负号显示成方块的问题
plt.rcParams['axes.unicode_minus'] = False


# 加载数据集
tips = sns.load_dataset("tips")


# 按星期分列的条形图
# 1. 搭建画布：按 'day'（星期）把数据拆分成多列子图
# height=4, aspect=0.5 决定了每个子图的高度为4英寸，宽度为 4*0.5=2英寸（比较窄长）
g = sns.FacetGrid(tips, col="day", height=4, aspect=0.5)

# 2. 填充图表：在每个子图中绘制条形图
# x轴为性别('sex')，y轴为总账单('total_bill')
# order=['Male', 'Female'] 强制指定了性别的排列顺序，完美避开了 UserWarning 警告
g.map(sns.barplot, "sex", "total_bill", order=['Male', 'Female'])
plt.show() # 每张图画完加个 show 方便查看


# 按星期分行且自定义排序的密度图
# 自定义排序（使用order参数）
# 1. 动态获取排序规则：按 'day' 在数据中出现的次数从多到少进行降序排列
ordered_days = tips.day.value_counts().index

# 2. 搭建画布：按 'day' 把数据拆分成多行子图
# row_order 确保了子图的排列顺序不是默认的字母序，而是按上面计算出的出现频率排序
g = sns.FacetGrid(tips, row="day", row_order=ordered_days, height=1.7, aspect=4)

# 3. 填充图表：在每个子图中绘制核密度估计图(KDE)，展示账单金额的分布曲线
g.map(sns.kdeplot, "total_bill")
plt.show()


# 按用餐时间分色的散点图
# 自定义颜色（使用调色板）
# 1. 定义调色板：创建一个字典，规定 Lunch(午餐)显示海绿色，Dinner(晚餐)显示深灰色(.7)
pal = dict(Lunch="seagreen", Dinner=".7")

# 2. 搭建画布：这次没有分行或分列，而是使用了 hue='time'
# 这意味着所有数据会画在同一张图上，但会根据 'time'（午餐/晚餐）区分颜色
g = sns.FacetGrid(tips, hue="time", palette=pal, height=5)

# 3. 填充图表：绘制散点图
# s=100 代表点的大小，alpha=0.5 代表点的透明度（防止重叠看不清）
g.map(sns.scatterplot, "total_bill", "tip", s=100, alpha=0.5)

# 4. 添加图例：因为用了 hue 分色，必须加上这句才会显示右上角的颜色说明
g.add_legend()
plt.show()