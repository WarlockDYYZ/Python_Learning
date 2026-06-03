# from __future__ import annotations
import pandas as pd
import numpy as np




# 构建示例销售数据集：包含门店、日期、逐日销售额
data = {
   'date': pd.date_range('2023-01-01', periods=12),  # 生成2023年1月的12个连续日期
   'store': ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B', 'A', 'B'],  # 两个门店交替出现
   'sales': [100, 120, 90, 110, 95, 130, 105, 125, 115, 140, 110, 135]  # 逐日销售额
}
sales_df = pd.DataFrame(data)
# 为后续时间窗口计算做准备：将时间列设为索引
# PyCharm 的类型检查器无法正确推断链式调用后的 DataFrame 类型, 其实可以写成一行的
sales_df = sales_df.set_index('date')
sales_df = sales_df.sort_index()
# pycharm 对 DataFrame 的类型判断有问题，也可能是因为版本的原因，反正不显示转换会有提示
print(sales_df.head(6).to_string())