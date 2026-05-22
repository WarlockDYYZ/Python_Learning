from bokeh.models import Slider, Column
from bokeh.plotting import figure, show
from bokeh.layouts import row
import numpy as np

from bokeh.server.server import Server  # 必须加
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler


def modify_doc(doc):
    # 创建滑块
    slider = Slider(start=0, end=10, value=1, title="Frequency")

    # 创建图表
    p = figure(x_range=(0, 10), y_range=(-2, 2))
    x = np.linspace(0, 10, 1000)
    y = np.sin(x)
    line = p.line(x, y, line_width=2)

    # 添加滑块回调
    def update_plot(attr, old, new):
        freq = slider.value
        line.data_source.data['y'] = np.sin(x * freq)

    slider.on_change('value', update_plot)
    
    # 组合布局
    layout = row(slider, p)
    doc.add_root(layout)


app = Application(FunctionHandler(modify_doc))
server = Server({'/': app}, port=5006)
server.start()

if __name__ == '__main__':
    print("打开浏览器访问：http://localhost:5006")
    server.run_until_shutdown()