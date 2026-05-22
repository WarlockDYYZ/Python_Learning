from bokeh.models import CustomJS, ColumnDataSource
from bokeh.plotting import figure, show

# 准备带有更多维度的数据
data = dict(
    x=[1, 2, 3, 4, 5],
    y=[6, 7, 2, 4, 5],
    size_val=[10, 20, 30, 40, 50],  # 用于动态映射大小的数据
    temp=[20, 25, 15, 30, 22],  # 用于动态映射颜色的数据
    label=['A', 'B', 'C', 'D', 'E']  # 用于悬停显示的标签
)
source = ColumnDataSource(data=data)

# 创建画布，并预先加入悬停工具(HoverTool)和平移缩放工具
p = figure(tools="pan,wheel_zoom,box_zoom,reset,hover,tap,box_select", width=500, height=400)

# 绘制高度定制的散点图
renderer = p.scatter(
    'x', 'y',
    source=source,
    marker="circle",  # 使用方形标记
    size="size_val",  # 动态映射：点的大小随 size_val 列变化
    fill_color="temp",  # 动态映射：点的颜色随 temp 列变化（此处简化演示，实际常配合线性配色）
    alpha=0.8,  # 整体透明度设为 0.8
    line_color="black",  # 边框设为黑色
    line_width=2,  # 边框加粗到 2 像素

    # 交互专属样式
    selection_color="red",  # 选中时变为红色
    nonselection_fill_color="lightgray",  # 未选中的点填充色变灰
    nonselection_alpha=0.2,  # 未选中的点透明度降为 0.2

    # 悬停专属样式
    hover_fill_color="orange",  # 鼠标悬停时变为橙色
    hover_alpha=1.0  # 悬停时完全不透明
)

# 配置悬停工具显示的具体内容
p.hover.tooltips = [
    ("索引", "$index"),
    ("坐标", "(@x, @y)"),
    ("标签", "@label"),
    ("当前大小", "@size_val")
]

# 添加点击事件回调
callback = CustomJS(
    args=dict(source=source),
    code="""
           // 在 source 的 selected 属性变化时，使用 cb_obj 来获取当前的选中对象
        const indices = cb_obj.indices;
        console.log('成功获取到选中的索引:', indices);
        """
)

# 原来的监听器绑定后不能显示 点击事件回调
# p.js_on_event('tap', callback)
source.selected.js_on_change('indices', callback)

show(p)
