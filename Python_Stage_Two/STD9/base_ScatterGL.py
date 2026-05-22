import numpy as np
from bokeh.plotting import figure, show
from bokeh.models import LinearColorMapper, ColorBar, ColumnDataSource
from bokeh.palettes import Viridis256


# 创建大规模散点图数据
N = 100000
x = np.random.random(N)
y = np.random.random(N)
z = np.random.randint(0, 100, N)

# 创建一个颜色映射器
# 用 z 的值来决定颜色深浅
color_mapper = LinearColorMapper(palette=Viridis256, low=min(z), high=max(z))

# 将数据封装到 ColumnDataSource 中
# Bokeh 在处理大量数据和动态映射时，强烈建议使用这种数据源格式
source = ColumnDataSource(data=dict(x=x, y=y, z=z))

p = figure(width=800, height=600, tools="pan,wheel_zoom,box_zoom,reset")

# 正确调用 color 参数
# 使用字典语法：'field' 指向数据源中的列名，'transform' 指向颜色映射器
p.scatter(
    'x', 'y',
    source=source,
    color={'field': 'z', 'transform': color_mapper},
    name='large_dataset'
    # Bokeh 的 scatter（散点图）方法没有 render_mode 参数
    # render_mode='webgl'
)

# 添加右侧的颜色条（ColorBar），让图表能看懂数值对应什么颜色
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=12, location=(0, 0))
p.add_layout(color_bar, 'right')

show(p)
