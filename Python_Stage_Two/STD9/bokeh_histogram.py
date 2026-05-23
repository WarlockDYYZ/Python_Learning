from bokeh.plotting import figure, show
import numpy as np


# 编写示例数据并处理
data = np.random.normal(0, 1, 1000)
# len(hist)=30 len(edges)=31
hist, edges = np.histogram(data, bins=30, density=True)
# print(hist)
# print(edges)

# 创建直方图
p = figure(
    tools="",                               # 暂时不添加内置工具
    width=800, height=600,
    title="Normal Distribution Histogram"   # 柱子左上角的标题
)

p.quad(
    top=hist,                               # 矩形的顶部高度对应之前算出的密度值
    bottom=0,                               # 矩形的底部固定在 0 刻度线
    left=edges[:-1], right=edges[1:],
    fill_color="skyblue",
    line_color="black"
)

p.xaxis.axis_label = 'Value'
p.yaxis.axis_label = 'Density'
p.grid.visible = False                      # 关掉了背景的网格线，让图表看起来更干净

show(p)                                     # 渲染并弹出浏览器窗口，展示出最终的交互式直方图
