import numpy as np
from bokeh.plotting import curdoc, figure
from bokeh.models import ColumnDataSource

# 初始化空的数据源
source = ColumnDataSource(data={'x': [], 'y': []})
data_count = 0

# 创建图表
p = figure(width=800, height=600, title="Real-time Data Streaming")
p.line('x', 'y', source=source, line_width=1, alpha=0.5)


# 定义周期性更新的回调函数（每隔100毫秒触发一次）
def update():
    global data_count
    if data_count >= 10000:  # 限制总点数，防止内存溢出
        return

    # 每次生成一小段新数据
    chunk_size = 100
    new_x = np.linspace(data_count, data_count + chunk_size, chunk_size)
    new_y = np.sin(new_x * 0.01) + np.random.normal(0, 0.1, chunk_size)

    # 使用 stream 方法将新数据“流”入图表
    source.stream({'x': new_x, 'y': new_y})
    data_count += chunk_size


# 将更新函数添加到文档的周期性任务中
curdoc().add_periodic_callback(update, 100)
# 将布局添加到当前文档
curdoc().add_root(p)