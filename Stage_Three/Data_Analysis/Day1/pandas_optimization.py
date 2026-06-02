import pandas as pd
import numpy as np


''' 数据清洗优化 '''
sales_df = pd.DataFrame()

# 避免就地修改
cleaned_df = sales_df.copy()

# 使用向量化操作代替循环
# 低效方法，循环遍历 + 索引不连续 + loc 动态赋值 = 必报错！
for i in range(len(cleaned_df)):
    if cleaned_df.loc[i, '销量'] > 0:
        cleaned_df.loc[i, '销售额'] = cleaned_df.loc[i, '销量'] * cleaned_df.loc[i, '单价']
# 高效方法,向量化计算
cleaned_df['销售额'] = np.where(cleaned_df['销量'] > 0, cleaned_df
['销量'] * cleaned_df['单价'], 0)

# 使用category类型优化内存
categorical_cols = ['地区', '产品类别', '客户等级']
cleaned_df[categorical_cols] = cleaned_df[categorical_cols].astype('category')
# pandas 明明支持同时转换多列类型，但编辑器的类型检查太严格，就报这个黄标。
# 循环逐列转换编辑器完全识别，无警告
# for col in categorical_cols:
#     cleaned_df[col] = cleaned_df[col].astype('category')

# 分块处理大数据
def process_large_data(file_path, chunksize=10000):
    chunks = []
    for chunk in pd.read_csv(file_path, chunksize=chunksize):
        # 数据清洗操作
        chunk['销售额'] = chunk['销量'] * chunk['单价']
        chunk['订单日期'] = pd.to_datetime(chunk['订单日期'])
        # 分组聚合
        chunk_grouped = chunk.groupby(['地区', '产品类别']).agg({
        '销量': 'sum',
        '销售额': 'sum'
        })
        chunks.append(chunk_grouped)
    return pd.concat(chunks).groupby(['地区', '产品类别']).sum()


''' 分组聚合优化 '''
grouped_df = pd.DataFrame()
# 避免使用apply函数
# 低效方法
grouped_df['销售额占比'] = grouped_df.apply(
lambda x: x['销售额'] / x['销售额'].sum()
)
# 高效方法
total_sales = grouped_df['销售额'].sum()
grouped_df['销售额占比'] = grouped_df['销售额'] / total_sales
# 使用transform进行组内计算
# 计算组内均值并广播回原数据
sales_df['地区销量均值'] = sales_df.groupby('地区')['销量'].transform('mean')
sales_df['季度销售额均值'] = sales_df.groupby('季度')['销售额'].transform('mean')


''' 透视表优化 '''
# 优化透视表性能
# 使用category类型优化分组键
sales_df['季度'] = sales_df['季度'].astype('category')
sales_df['地区'] = sales_df['地区'].astype('category')
# 预先计算聚合值
aggregated_df = sales_df.groupby(['季度', '地区'])['销售额'].sum().reset_index()
# 使用透视表重塑结构
pivot_table_optimized = pd.pivot_table(
data=aggregated_df,
values='销售额',
index='季度',
columns='地区',
aggfunc='sum',
fill_value=0
)
# 处理透视表中的空值
pivot_table_optimized.fillna(0, inplace=True)
# 使用多线程处理
from joblib import Parallel, delayed


# 定义分组聚合函数
def group_by_category(chunk):
    return chunk.groupby('产品类别').agg({
    '销量': 'sum',
    '销售额': 'sum'
    })


# 并行处理
results = Parallel(n_jobs=-1, backend='threading')(
delayed(group_by_category)(chunk) for chunk in pd.read_csv('large_sales_data.csv', chunksize=10000)
)
# 合并结果
final_result = pd.concat(results).groupby('产品类别').sum()