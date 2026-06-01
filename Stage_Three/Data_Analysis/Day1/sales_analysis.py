import pandas as pd
import numpy as np

from Stage_Three.Data_Analysis.Day1.about_merge import merged_df

# 加载销售数据
sales_df = pd.read_csv('sales_data.csv', encoding='utf-8-sig')
# 检查数据质量
print(sales_df.info())
print(sales_df.isnull().sum())


# 预处理
# 处理缺失值
sales_df['订单日期'] = pd.to_datetime(sales_df['订单日期'], errors='coerce')
sales_df['折扣率'] = sales_df['折扣率'].fillna(1.0)
# 处理重复值
sales_df.drop_duplicates(subset=['订单ID', '产品ID'], inplace=True)
# 创建新特征
sales_df['销售额'] = sales_df['单价'] * sales_df['销量'] * sales_df
['折扣率']
sales_df['年份'] = sales_df['订单日期'].dt.year
sales_df['季度'] = sales_df['订单日期'].dt.quarter
sales_df['月'] = sales_df['订单日期'].dt.month_name(lang='zh-tw')()
# 转换数据类型
sales_df['客户ID'] = sales_df['客户ID'].astype('category')
sales_df['产品类别'] = sales_df['产品类别'].astype('category')
sales_df['地区'] = sales_df['地区'].astype('category')


# 分组聚合分析
# 按地区和产品类别分组聚合
grouped_region_product = sales_df.groupby(['地区', '产品类别'])
# 计算基本指标
aggregation_dict = {
    '销量': ['sum', 'mean', 'count'],
    '销售额': ['sum', 'mean', 'std'],
    '单价': ['min', 'max', 'mean'],
    '折扣率': ['mean', 'std']
}
# 应用聚合函数
region_product_metrics = grouped_region_product.agg(aggregation_dict)
region_product_metrics.columns = region_product_metrics.columns.map(' '.join)
print(region_product_metrics.head())


# 透视表创建
# 创建地区×季度的销售透视表
region_quarter_pivot = pd.pivot_table(
    data=sales_df,
    values='销售额',
    index='地区',
    columns=sales_df['季度'],
    aggfunc='sum',
    fill_value=0,
    margins=True,
    margins_name='总计'
)
# 创建多层透视表
multi_pivot = pd.pivot_table(
    data=sales_df,
    values=['销售额', '销量'],
    index=['地区', '城市'],
    columns=['季度', '产品类别'],
    aggfunc='sum',
    fill_value=0,
    margins=True,
    margins_name='总计'
)
# 透视表转换
flattened_pivot = multi_pivot.reset_index()  # 展开索引
stacked_pivot = multi_pivot.stack(0)  # 按第一层索引堆叠


# 交叉表分析
# 产品类别与季度的交叉销售
cross_table = pd.crosstab(
    index=sales_df['产品类别'],
    columns=sales_df['季度'],
    values=sales_df['销售额'],
    aggfunc='mean'
)
# 按季度计算各产品类别的销售占比
cross_table_normalize = pd.crosstab(
    index=sales_df['产品类别'],
    columns=sales_df['季度'],
    values=sales_df['销售额'],
    aggfunc='sum',
    normalize='columns'  # 按季度计算百分比
)
# 按产品类别计算季度销售趋势
cross_table_trend = pd.crosstab(
    index=sales_df['产品类别'],
    columns=sales_df['季度'],
    values=sales_df['销售额'],
    aggfunc=lambda x: (x - x.mean()) / x.std()  # 计算Z值
)


# 数据合并应用
# 加载客户数据
customer_df = pd.read_csv('customer_data.csv', encoding='utf-8-sig')
# 内连接：获取有销售记录的客户信息
merged_df = pd.merge(
    sales_df,
    customer_df,
    on='客户ID',
    how='inner'
)
# 横向合并：将季度销售数据与客户数据合并
concatenated_df = pd.concat(
    [merged_df, customer_df],
    axis=1,
    join='inner'
)
# 基于索引的连接
merged_df.set_index('客户ID', inplace=True)
customer_df.set_index('客户ID', inplace=True)
joined_df = merged_df.join(customer_df, how='left')


# 可视化
# 导出为Excel文件
with pd.ExcelWriter('分析报告.xlsx', engine='xlsxwriter') as writer:
    # 导出透视表
    region_quarter_pivot.to_excel(writer, sheet_name='地区季度销售')
    # 导出交叉表
    cross_table.to_excel(writer, sheet_name='产品季度交叉')
    # 导出合并数据
    merged_df.to_excel(writer, sheet_name='合并销售客户', index=False)

# 设置条件格式
workbook = writer.book
format_red = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
format_green = workbook.add_format({'bg_color': '#D8E4BC', 'font_color': '#226600'})

# 获取透视表工作表
ws_pivot = writer.sheets['地区季度销售']
# 高亮最高销售额
ws_pivot.conditional_format('C2:G7', {
    'type': 'cell',
    'criteria': '>=',
    'value': 100000,
    'format': format_red
})
# 获取交叉表工作表
ws_cross = writer.sheets['产品季度交叉']
# 高亮季度变化
for col_num in range(2, ws_cross.ncols):
    ws_cross.conditional_format(0, col_num, ws_cross.nrows, col_num, {
    'type': 'cell',
    'criteria': '>=',
    'value': 100000,
    'format': format_red
})

# 导出为CSV文件
sales_df.to_csv('清洗销售数据.csv', index=False)