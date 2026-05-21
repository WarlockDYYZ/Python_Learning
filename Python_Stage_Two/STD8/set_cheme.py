import seaborn as sns
import matplotlib.pyplot as plt


# 设置全局字体为“微软雅黑”（Windows系统自带）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# 解决负号显示成方块的问题
plt.rcParams['axes.unicode_minus'] = False
# 加载数据集
tips = sns.load_dataset("tips")


# 第一张图：白色网格主题
sns.set_theme(style="whitegrid")
sns.scatterplot(data=tips, x="total_bill", y="tip")
plt.title("Theme: whitegrid") # 加个标题方便区分
plt.show()      # 立即渲染并弹出第一张图
plt.close()     # 关闭当前画布，防止下一张图重叠上来

# 第二张图：深色主题
sns.set_theme(style="dark")
sns.scatterplot(data=tips, x="total_bill", y="tip")
plt.title("Theme: dark")
plt.show()
plt.close()

# 第三张图：带刻度主题
sns.set_theme(style="ticks")
sns.scatterplot(data=tips, x="total_bill", y="tip")
plt.title("Theme: ticks")
plt.show()
plt.close()

# 第四张图：临时设置纯白主题
with sns.axes_style("white"):
    plt.figure(figsize=(6, 6))
    sns.scatterplot(data=tips, x="total_bill", y="tip")
    plt.title("Theme: white (temporary)")
plt.show()
plt.close()


# 自定义样式参数
sns.set_style("darkgrid", {
    "axes.facecolor": ".9",  # 设置背景颜色
    "axes.grid": True,       # 显示网格
    "grid.color": "white",   # 网格颜色
    "grid.linestyle": "--"   # 网格线型
})
sns.scatterplot(data=tips, x="total_bill", y="tip")
plt.show()
plt.close()

# 移除顶部和右侧边框
sns.set_style("ticks")
sns.scatterplot(data=tips, x="total_bill", y="tip")
sns.despine()  # 自动隐藏图表顶部（top）和右侧（right）的边框
# sns.despine(offset=10)  # 让左侧和下侧的坐标轴线与图表内容产生 10 像素的距离，显得更透气
# sns.despine(left=True, bottom=True)  # 隐藏所有边框
plt.show()
plt.close()

plt.show()

