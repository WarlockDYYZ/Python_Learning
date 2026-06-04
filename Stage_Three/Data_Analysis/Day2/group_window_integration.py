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
# PyCharm 对 DataFrame 的类型判断有问题，也可能是因为版本的原因，反正不显示转换会有提示
print(sales_df.head(6).to_string())


print("\n\n分组滚动窗口")
# 核心逻辑：先按门店分组，再对每个分组内的销售额应用3日滚动窗口计算
# reset_index(0, drop=True) 用于清理分组索引，将结果合并回原始DataFrame
sales_df['rolling_avg_sales'] = sales_df.groupby('store')['sales'].rolling(window=3, min_periods=1).mean().reset_index(0, drop=True)
print(sales_df.head(6).to_string())


print("\n\n分组扩展窗口")
# 核心逻辑：先按门店分组，再对每个分组内的销售额应用扩展窗口计算
sales_df['expanding_sum_sales'] = sales_df.groupby('store')['sales'].expanding(min_periods=1).sum().reset_index(0, drop=True)
print(sales_df.head(6).to_string())


print("\n\n分组指数加权窗口")
# 核心逻辑：先按门店分组，再对每个分组内的销售额应用指数加权窗口计算
# span=5：权重衰减幅度为5，对近期销售数据的敏感度更高
# 代码不变，只加注释压制警告 IDE 的问题，，对 ewm()
# noinspection PyUnresolvedReferences
sales_df['ewm_sales'] = sales_df.groupby('store')['sales'].ewm(span=5).mean().reset_index(0, drop=True)
print(sales_df.head(6).to_string())


print("\n\n自定义聚合函数")


# 步骤1：定义自定义聚合函数
def trimmed_mean(x):
    """
        计算截尾均值：剔除窗口内的最大值和最小值后，计算剩余数据的平均值
        x: 窗口内的 Series 数据
    """
    if len(x) <= 2:  # 若窗口内的有效数据行数不足3行，则直接返回原始数据的平均值
        return x.mean()
    # 剔除最大值和最小值后，计算剩余数据的平均值
    return (x.sum() - x.max() - x.min()) / (len(x) - 2)


# 步骤2：先按门店分组，再对每个分组内的销售额应用自定义窗口函数
sales_df['trimmed_mean_sales'] = sales_df.groupby('store')['sales'].rolling(window=3, min_periods=1).apply(trimmed_mean).reset_index(0, drop=True)
print(sales_df.head(6).to_string())

