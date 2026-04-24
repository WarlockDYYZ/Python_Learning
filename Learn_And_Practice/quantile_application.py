import pandas as pd
import numpy as np

excel_path = r"C:\Users\Administrator\Desktop\Daily_Report\二三线业务情况.xlsx"
# 1. 读取 Excel 文件为 DataFrame
# pd.read_excel() 方法用于从 Excel 文件中读取数据并加载为 DataFrame。它支持读取 .xls 和 .xlsx 格式的文件
# read_excel 默认读取第一个表单（sheet_name=0），假设 data.xlsx 文件中只有一个表单，读取后的数据会存储在一个 DataFrame 中
# 如果 data.xlsx 文件中有多个表单，可以通过指定 sheet_name 来读取特定表单的数据
# 例如 pd.read_excel('data.xlsx', sheet_name='Sheet1')

# 这告诉 Pandas: 跳过第 0 行，使用第 1 行（即 Excel 中的第二行）作为列名
df = pd.read_excel(excel_path, header=1)

# 一个小测试 输出
# 2. 通过列名提取 Series
# 假设 Excel 中有一列名为 '日期'
# series_data = df['日期']
# 输出该列 除第一行以外的数据
# print(series_data)
# 验证类型
# print(type(series_data))
# 输出: <class 'pandas.core.series.Series'>

# 小测试 切片
# df_2 = df[:]
# print(df_2)
# print(df["有效通话量"])

# 遍历 DataFrame 的每一列
# for column_name, series_data in df.items():
#     print(f"列名: {column_name}")
#     print(f"数据类型: {type(series_data)}")
#     # 这里 type(series_data) 永远是 pandas.core.series.Series
#     print("-" * 20)

# 1. 剔除前三列
# 方法 A: 使用 iloc，从第 7 列（索引为7，即“姓名”列）开始截取到最后
# 从0开始姓名在第7列, 从第7列开始切片，表头有一个提示行已在上方
# header=1时剔除
df_clean = df.iloc[:, 7:]

# 2. 将“姓名”作为 Series 的名字（即索引）
# 设置索引后，姓名就不再是普通数据列，而是行标签，转置以获得需要的数据格式
# （excel表中姓名为列，数据在对应的行，转置后每个Series的名字正好是姓名，数据是对应的值）
series_result = df_clean.set_index('姓名').T

# 如果你只需要从 0 开始的数字序号，不再需要保留左侧的时间列，直接加上 drop=True 参数
series_result = series_result.reset_index(drop=True)

# 此处不使用顺便了解
# 如果你希望时间信息不消失，而是变成表格中的第一列数据（列名通常默认为 index 或 date），则不需要加 drop 参数（或者设置为 False）
# 重置索引，原来的时间索引会变成第一列数据
# df_reset = df.reset_index()
# 如果你希望序列从 1 开始而不是 0，可以在重置后手动修改索引
# df_reset.index = df_reset.index + 1

# 计算前的准备
# 在 Pandas 中处理 NaN（缺失值）和 0（零值）的策略完全不同 区分
# NaN: 通常表示“数据缺失”或“未记录”
# Pandas 的统计函数（如 quantile、mean）默认会自动忽略它们，所以通常不需要特殊处理
# 0: 表示“数值为零”
# 在计算分位数或平均值时，0 会被当作真实数据参与计算（这会拉低平均值和中位数）
# 如果想消除它的影响，必须显式地将其转换为 NaN

# 方法: 将所有的 0 替换为 NaN
df_clean = series_result.replace(0, np.nan)
# 仅为方便查看数据，输出为excel，不做实际输出
# df_clean.to_excel('output.xlsx', sheet_name='Sheet1', index=False)

# df_clean.head()
# 快速预览数据的前几行，确认数据清洗或处理后的结果是否符合预期
# 默认5行，可加参数调整, 如: df_clean.head(10)
# print(df_clean.head())

# 计算前准备的准备
# 碎碎念: 我们概率论的老师真的讲过，我有印象，确实忘了怎么算了，也可能刚开始就不知道
# 边学边学嘛
# 以第一行数据为例
# 23个数字3个空值，有效数有20个
# 排序后的数据（共20个）: 
# 37, 70, 83, 85, 88, 96, 99, 100, 102, 109, 112, 114, 119, 122, 123, 123, 125, 133, 147, 175
# Pandas 使用的默认算法（线性插值法）计算位置的公式是: 
# 位置 = 1+(N-1) x 百分比
# 其中 N = 20

# 第一四分位数 (Q1 / 25%) = 94
# 计算位置 = 1 + (20−1) × 0.25 = 1 + 4.75 = 5.75
# 这说明 Q1 的值位于第 **5** 个数和第 **6** 个数之间，且更靠近第 6 个数（0.75 的位置）
# 锁定数值: 
# 第 5 个数: 88
# 第 6 个数: 96
# 线性插值计算: Q1 = 88 + (96−88) × 0.75
#                = 88 + 8 × 0.75 = 94

# 第二四分位数 (Q2 / 50%) = 110.5
# 计算位置 = 1 + (20−1) × 0.5 = 1 + 9.5 = 10.5
# 这说明 Q1 的值位于第 **10** 个数和第 **11** 个数之的正中间
# 锁定数值:
# 第 10 个数: 109
# 第 11 个数: 112
# 线性插值计算: Q2 = 109 + (112-109) × 0.5
#                = 109 + 3 × 0.5 = 110.5

# 第三四分位数 (Q3 / 75%) =
# 计算位置 = 1 + (20−1) × 0.75 = 1 + 14.25 = 15.25
# 这说明 Q3 的值位于第 **15** 个数和第 **16** 个数之间，但非常靠近第 15 个数（0.25 的位置）
# 锁定数值:
# 第 15 个数: 123
# 第 16 个数: 123
# 线性插值计算: Q1 = 123 + (123-123) × 0.25
#                = 123 + 0 × 0.25 = 123
# *(注：因为第15和16个数恰好相同，所以无论怎么插值，结果都是123)*

quantiles = df_clean.quantile([0.25, 0.5, 0.75])

# 查看输出
# print(quantiles)

final_result = quantiles.T
final_result.columns = ['Q1', 'Q2', 'Q3']
final_result['IQR'] = final_result['Q3'] - final_result['Q1']
final_result.to_excel(r'C:\Users\Administrator\Desktop\TTT\output1.xlsx', sheet_name='Sheet1', index=True)
# print(final_result)

###########################################################################################################
# 奖励给读到代码末尾的人的注释，大概一分钟前我查资料的时候发现，该函数的语法(大概率是官方的)为:                            #
# DataFrame.quantile(q=0.5, axis=0, numeric_only=False, interpolation='linear', method='single')          #
#                                                                                                         #
# q:float 或 list-like, 默认值是 0.5                                                                        #
#   需要计算的分位数,可以是一个浮点数(如 0.25 表示 25% 分位数), 也可以是一个列表(如 [0.25, 0.5, 0.75] 表示多个分位数)   #
#                     #####################################################                               #
# axis: int默认值是0   # 早知道可以按行计算，我还花功夫转置，干什么，虽然确实理解深刻了 #                              #
#                     #####################################################                               #
#   指定计算分位数的轴: 0 表示按列计算分位数，1 表示按行计算分位数                                                  #
# numeric_only：bool，默认值是 False                                                                        #
#   是否只计算数值类型的列。默认为 False，即计算所有列(如果 True，会忽略非数值类型的列)                                #
# interpolation：str，默认值是 'linear'                                                                     #
#   当数据点不完全匹配时的插值方法 'linear'、      'lower'、'higher'、'midpoint' 或 'nearest'                    #
#                             i+(i+j)*分数部分    i        j      (i+j)/2      最近 (没具体查,还是查了后来)     #
# method: {‘single’, ‘table’}, 默认值 ‘single’                                                             #
#   是计算每列的分位数 (‘single’) 还是计算所有列的分位 (‘table’)                                                 #
#   当使用 ‘table’, 唯一允许的插值方法是 ‘nearest’, ‘lower’, and ‘higher’                                      #
###########################################################################################################
