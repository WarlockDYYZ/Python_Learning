from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource
from bokeh.models.layouts import TabPanel, Tabs
from bokeh.models.widgets import DataTable, TableColumn, NumberFormatter
from bokeh.layouts import column, row
import pandas as pd
import numpy as np
from bokeh.models import Span

# 创建财务数据
transactions = {
    'Date': pd.date_range('2024-01-01', periods=30),
    'Category': ['Food', 'Transport', 'Shopping', 'Bills', 'Entertainment'] * 6,
    'Amount': np.random.uniform(10, 200, 30),
    'Type': ['Expense'] * 30
}
df = pd.DataFrame(transactions)

# 创建数据源
source = ColumnDataSource(df)


# 创建支出分类饼图
def create_pie_chart():
    category_summary = df.groupby('Category')['Amount'].sum()
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
    p = figure(height=350, width=350, title="Expense Distribution by Category")

    angles = []
    start_angle = 0
    total = df['Amount'].sum()

    for i, (category, amount) in enumerate(category_summary.items()):
        angle = 2 * np.pi * amount / total
        angles.append((start_angle, start_angle + angle))
        start_angle += angle
        p.wedge(x=0, y=0, radius=0.3,
                start_angle=angles[i][0], end_angle=angles[i][1],
                line_color="white", line_width=2,
                fill_color=colors[i], legend_label=category)

    p.axis.visible = False
    p.grid.visible = False
    p.legend.location = "right"
    return p


# 创建支出趋势图
def create_trend_chart():
    p = figure(width=800, height=350,
               x_axis_type='datetime', title="Daily Expense Trend")

    # ✅ 加了 legend_label，图例就生效了
    p.line(df['Date'], df['Amount'], line_width=2, color='#1f77b4', legend_label="Daily Expense")
    p.scatter(df['Date'], df['Amount'], size=8, color='#ff7f0e', alpha=0.7)

    # 添加平均线
    avg_expense = df['Amount'].mean()

    hline = Span(
        location=avg_expense,
        dimension='width',
        line_color='red',
        line_dash='dashed',
        line_width=2
    )

    p.add_layout(hline)
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Amount (USD)'
    p.legend.location = 'top_left'
    p.grid.visible = True
    p.grid.grid_line_alpha = 0.3
    return p


# 创建交易数据表
def create_transactionTable():
    columns = [
        TableColumn(field='Date', title='Date', formatter=NumberFormatter(format='%Y-%m-%d')),
        TableColumn(field='Category', title='Category'),
        TableColumn(field='Amount', title='Amount (USD)',
                    formatter=NumberFormatter(format='$0,0.00')),
        TableColumn(field='Type', title='Type')
    ]
    data_table = DataTable(source=source, columns=columns,
                           width=800, height=200)
    return data_table


# 创建选项卡布局
tab1 = TabPanel(child=create_pie_chart(), title="Expense Distribution")
tab2 = TabPanel(child=create_trend_chart(), title="Daily Trend")
tab3 = TabPanel(child=create_transactionTable(), title="Transaction History")
tabs = Tabs(tabs=[tab1, tab2, tab3])

# 创建总支出显示
total_expense = df['Amount'].sum()
total_display = figure(width=300, height=100,
                       toolbar_location=None,
                       title=f"Total Expense: ${total_expense:.0f}")

total_display.axis.visible = False
total_display.grid.visible = False

# 加一个空白矩形，让图表不为空，消除警告
total_display.rect(x=0, y=0, width=1, height=1, alpha=0)

# 组合布局
layout = column(row(tabs, total_display))

# 显示仪表板
output_file("personal_finance_dashboard.html")
show(layout)
