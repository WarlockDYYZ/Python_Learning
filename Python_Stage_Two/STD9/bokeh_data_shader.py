import numpy as np
import pandas as pd
import datashader as ds
import datashader.transfer_functions as tf
from bokeh.plotting import figure, show, output_file
from bokeh.models import Range1d, ColumnDataSource, CustomJS


# 1. 准备数据 (100万个点)
N = 1000000
np.random.seed(42)
x = np.random.normal(size=N)
y = np.random.normal(size=N)
df = pd.DataFrame({'x': x, 'y': y})

# 2. 创建 Bokeh 图表
p = figure(tools="pan,wheel_zoom,box_zoom,reset", width=800, height=600,
           x_range=Range1d(-5, 5), y_range=Range1d(-5, 5),
           title="百万级散点图交互 (双击运行HTML)")

# 3. 添加一个空的 image_rgba 图层，用于存放渲染后的图像
# 注意：这里先给一个空数组占位
img_source = ColumnDataSource(data=dict(image=[[]], x=[-5], y=[-5], dw=[10], dh=[10]))
p.image_rgba(source=img_source, image='image', x='x', y='y', dw='dw', dh='dh')


# 4. 生成初始图像数据 (将 DataFrame 转为 JSON 传递给 JS)
def create_image_data(x_range, y_range, width, height):
    cvs = ds.Canvas(plot_width=width, plot_height=height, x_range=x_range, y_range=y_range)
    agg = cvs.points(df, 'x', 'y', ds.count())
    img = tf.shade(agg, cmap=['red', 'yellow', 'green'])
    # 转换为 NumPy 数组并处理格式
    img_data = np.flipud(np.array(img.to_pil().convert('RGBA')))
    return img_data.view(dtype=np.uint32).reshape(height, width)


# 初始渲染
initial_data = create_image_data((-5, 5), (-5, 5), 800, 600)
img_source.data['image'] = [initial_data]
img_source.data['dw'] = [10]
img_source.data['dh'] = [10]

# 5. 编写 JavaScript 回调代码 (CustomJS)
# 这段代码会在浏览器中运行，不需要 Python 环境
js_code = """
    // 获取当前视图范围
    const x_start = cb_obj.start;
    const x_end = cb_obj.end;
    const y_start = cb_obj.start;
    const y_end = cb_obj.end;

    // 获取画布尺寸
    const width = plot.width;
    const height = plot.height;

    // 计算当前视图的跨度
    const x_range = x_end - x_start;
    const y_range = y_end - y_start;

    // 如果范围太小或太大，不更新（防止卡顿）
    if (x_range < 1e-6 || y_range < 1e-6) return;

    // 这里简化处理：直接拉伸之前的图像（实际上应该重新计算直方图）
    // 由于 Datashader 的 JS 版本较难集成，这里演示逻辑：更新图像位置和大小
    // 在实际生产环境中，你可能需要预加载数据或使用更复杂的 WASM 方案
    // 这里仅演示 Bokeh 的交互逻辑框架

    // 更新图像源的数据范围
    source.data.x = [x_start];
    source.data.y = [y_start];
    source.data.dw = [x_range];
    source.data.dh = [y_range];

    // 模拟数据更新 (这里只是简单拉伸，实际应调用 datashader.js)
    // 为了演示，我们只更新位置，不重新渲染像素
    source.change.emit();
"""

# 6. 绑定 JavaScript 回调
# 当 x_range 或 y_range 发生变化时，执行上面的 JS 代码
callback = CustomJS(args=dict(source=img_source, plot=p), code=js_code)
p.x_range.js_on_change('start', callback)
p.x_range.js_on_change('end', callback)
p.y_range.js_on_change('start', callback)
p.y_range.js_on_change('end', callback)

# 7. 输出文件并显示
output_file("interactive_datashader.html", title="Interactive Plot")
show(p)