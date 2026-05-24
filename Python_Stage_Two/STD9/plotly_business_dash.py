import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# 创建Dash应用
app = dash.Dash(__name__)

# 模拟商业数据
data = {
    'Year': ['2020', '2021', '2022', '2023', '2024'],
    'Revenue': [100, 120, 135, 150, 165],
    'Profit': [15, 18, 22, 25, 28],
    'Expenses': [85, 102, 113, 125, 137]
}
df = pd.DataFrame(data)

# 应用布局
app.layout = html.Div([
    html.Div([
        html.H1("Business Performance Dashboard",
                style={'textAlign': 'center', 'margin': '20px 0'}),
        # 关键指标卡片
        html.Div([
            html.Div([
                html.H3("Revenue", style={'textAlign': 'center'}),
                html.H2("$165M", style={'textAlign': 'center', 'fontSize': '24px', 'fontWeight': 'bold'})
            ], className="card"),
            html.Div([
                html.H3("Profit", style={'textAlign': 'center'}),
                html.H2("$28M", style={'textAlign': 'center', 'fontSize': '24px', 'fontWeight': 'bold'})
            ], className="card"),
            html.Div([
                html.H3("Profit Margin", style={'textAlign': 'center'}),
                html.H2("16.97%", style={'textAlign': 'center', 'fontSize': '24px', 'fontWeight': 'bold'})
            ], className="card"),
        ], className="row"),
        # 主要图表
        html.Div([
            dcc.Graph(id='revenue-trend'),
            dcc.Graph(id='profit-analysis')
        ], className="row"),
        # 交互式控件
        html.Div([
            html.Label("Select Year Range:"),
            dcc.RangeSlider(
                id='year-slider',
                min=2020,
                max=2024,
                step=1,
                value=[2020, 2024],
                marks={str(year): str(year) for year in range(2020, 2025)}
            )
        ], style={'margin': '20px 0'})
    ])
], style={'padding': '20px', 'fontFamily': 'Arial'})


# 回调函数更新图表
@app.callback(
    [Output('revenue-trend', 'figure'),
     Output('profit-analysis', 'figure')],
    [Input('year-slider', 'value')]
)
def update_charts(selected_years):
    mask = (df['Year'] >= str(selected_years[0])) & (df['Year'] <= str(selected_years[1]))
    filtered_df = df[mask]
    # 创建收入趋势图
    fig1 = px.line(filtered_df, x='Year', y='Revenue',
                   title='Revenue Trend', markers=True, line_shape='linear')
    fig1.update_layout(showlegend=False, yaxis_title='Revenue (Million USD)')
    # 创建利润分析图
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=filtered_df['Year'], y=filtered_df['Revenue'],
                          name='Revenue', marker_color='#1f77b4'))
    fig2.add_trace(go.Bar(x=filtered_df['Year'], y=filtered_df['Expenses'],
                          name='Expenses', marker_color='#ff7f0e'))

    # 新版：go.Scatter + mode='lines' 替换旧的 go.Line
    fig2.add_trace(go.Scatter(
        x=filtered_df['Year'],
        y=filtered_df['Profit'],
        name='Profit',
        line=dict(color='green', width=3),
        mode='lines'  # 必须加
    ))

    fig2.update_layout(
        title='Profit and Loss Analysis',
        barmode='stack',
        yaxis_title='Amount (Million USD)'
    )

    return fig1, fig2


if __name__ == '__main__':
    app.run(debug=True)
