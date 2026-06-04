import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# 全局设置：统一时间显示格式，避免不同环境的格式差异
# 1.日期全局显示
if hasattr(pd.options.display, "datetime_format"):
    pd.options.display.datetime_format = "%Y-%m-%d"  # 如需时分秒："%Y-%m-%d %H:%M:%S"

# 2.关闭日月颠倒
pd.options.display.date_dayfirst = False
pd.options.display.date_yearfirst = False
# 3.浮点数统一2位，消除pycharm类型警告
pd.options.display.float_format = lambda x: f"{x:.2f}"

# 准备示例销售数据
data = {
   'date': pd.date_range('2023-01-01', periods=4),
   'store': ['A', 'A', 'B', 'B'],
   'sales': [100, 120, 80, 90]
}
df = pd.DataFrame(data)

# 【常规分组聚合】：按门店分组，计算每个门店的总销售额
# 结果：每个门店对应1行记录，数据行数被压缩
grouped_sum = df.groupby('store')['sales'].sum().reset_index()
print(grouped_sum)

# 【窗口函数】：按门店分组，计算每个门店的逐日累计销售额（保留所有原始行）
# 结果：保留原始的4行记录，同时在新列中显示每个门店的逐日累计销售额
df['cumulative_sales'] = df.groupby('store')['sales'].cumsum()
print(df)
