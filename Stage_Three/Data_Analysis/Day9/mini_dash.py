# 1. 导入依赖库
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc


# 2. 初始化Dash应用
# 这里引入Bootstrap的FLATLY主题，快速实现现代化响应式样式
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

import plotly.express as px

# 1. 用 Plotly Express 创建图表（自动识别类型）
fig = px.bar(
    x=['1月', '2月', '3月'],
    y=[120, 150, 180],
    title='示例月度数据对比',
    color_discrete_sequence=['#3498db']  # 自定义颜色
)

# 3. 定义应用布局（页面结构）
app.layout = html.Div([
    # 标题组件
    html.H1("我的第一个Dash应用", style={"textAlign": "center", "color": "#2c3e50"}),
    # 分割线
    html.Hr(),
    # 文本描述组件，text-muted 柔和或次要的文本
    html.P("恭喜你成功运行Dash应用！", className="text-center text-muted"),
    # 核心图表组件（这里展示一个简单的柱状图）
    dcc.Graph(
        figure=fig
    )
])

# 4. 启动应用
if __name__ == '__main__':
    # debug=True开启热更新，修改代码后页面将自动刷新；默认端口为8050
    app.run(debug=True)