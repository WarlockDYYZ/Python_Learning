import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 模拟生成销售数据：生成4个门店的90天逐日销售数据，覆盖2个区域
np.random.seed(42)
# 生成90个连续日期作为销售日期
dates = pd.date_range('2023-01-01', periods=90, freq='D')
# 生成门店ID列表：4个门店，每个门店重复出现90天
stores = np.repeat(['Store_A', 'Store_B', 'Store_C', 'Store_D'], 90)
# 生成区域列表：Store_A和Store_B属于区域1，Store_C和Store_D属于区域2
regions = np.repeat(['Region_1', 'Region_2'], 180)
# 生成逐日销售额数据：基础趋势+每周的季节性波动+随机噪音
sales = np.tile(100 + np.arange(90)*0.5 + 10*np.sin(np.arange(90)*2*np.pi/7), 4) + np.random.normal(0, 5, 360)
# 将数据封装为DataFrame
sales_df = pd.DataFrame({
    'date': np.tile(dates, 4),  # 重复日期列表，匹配4个门店的90天数据
    'store': stores,
    'region': regions,
    'sales': sales
})

# 2. 数据预处理：将日期列设为datetime类型并排序
sales_df['date'] = pd.to_datetime(sales_df['date'])
# 设为时间索引，为后续时间窗口计算做准备
# 设置索引
sales_df = sales_df.set_index('date')
sales_df = sales_df.sort_index()
print(sales_df.head().to_string())

# 3. 分组窗口计算：先按门店分组，再在每个分组内应用滚动窗口、扩展窗口计算
# noinspection PyUnresolvedReferences
sales_df['7d_avg_sales'] = sales_df.groupby('store')['sales'].transform(
    lambda x: x.rolling(window='7D', min_periods=1).mean()
)
print(sales_df.head().to_string())
#
# # 4. 分组扩展窗口计算：计算每个门店的逐日累计销售额
# sales_df['cumulative_sales'] = sales_df.groupby('store')['sales'].expanding(min_periods=1).sum().reset_index(0, drop=True)
#
# # 5. 查看每个门店的核心统计结果
# # 提取每个门店的最后一条记录，得到最终的累计销售额和7日滚动平均销售额
# final_stats = sales_df.groupby('store')[['sales', '7d_avg_sales', 'cumulative_sales']].last()
# print(final_stats.to_string())
#
# # 6. 可视化：对比不同门店的7日滚动平均销售额趋势
# plt.figure(figsize=(12, 6))
# for store in sales_df['store'].unique():
#     store_data = sales_df[sales_df['store'] == store]
#     plt.plot(store_data.index, store_data['7d_avg_sales'], label=store)
# plt.title('各门店7日滚动平均销售额趋势对比')
# plt.legend()
# plt.show()