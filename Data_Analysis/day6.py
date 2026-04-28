import nltk
import pandas as pd
import numpy as np
import datetime
import re
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

import nltk

try:
    from nltk.corpus import stopwords
except:
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')


# 数据输入输出
def print_dot():
    print(100 * ".")


def print_star():
    print(100 * "*")


# 4.1 CSV 文件的读取与写入
# CSV（逗号分隔值）是最常用的数据交换格式之一,Pandas 提供了强大的 CSV 文件处理功能
# 读取CSV文件
# 使用pd.read_csv()函数读取CSV文件
# 读取CSV文件（最简单方式）
df_csv = pd.read_csv('data.csv')
print("读取CSV文件（默认参数）:")
print(df_csv.head())  # 显示前5行
# 读取CSV文件并指定参数
df_csv_params = pd.read_csv(
    'data.csv',
    sep=',',  # 分隔符（默认是逗号）
    header=0,  # 指定哪一行作为列名（0表示第一行）
    index_col=None,  # 指定索引列（None表示不使用某列为索引）
    usecols=None,  # 指定读取哪些列（None表示全部列）
    nrows=None,  # 读取的行数（None表示全部）
    skiprows=None,  # 跳过的行数
    na_values=['NA', 'N/A', 'None'],  # 识别为缺失值的字符串
    parse_dates=['Date'],  # 将指定列解析为日期
    encoding='utf-8'  # 文件编码
)
print("读取CSV文件（指定参数）:")
print(df_csv_params.info())
print_dot()

# 写入CSV文件
# 使用DataFrame.to_csv()方法写入CSV文件
# # 创建示例DataFrame
df_to_csv = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'Score': [85.5, 90.0, 78.5, 88.0],
    'City': ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen']
})
# 写入CSV文件（最简单方式）
df_to_csv.to_csv('output.csv', index=False)
print("写入CSV文件（默认参数）:")
print("文件已保存到output.csv")
# 写入CSV文件并指定参数
df_to_csv.to_csv(
    'output_with_params.csv',
    sep=',',  # 分隔符
    na_rep='N/A',  # 缺失值的表示方式
    float_format='%.1f',  # 浮点数格式
    index=True,  # 是否包含索引（默认True）
    header=True,  # 是否包含列名（默认True）
    columns=['Name', 'Age', 'City'],  # 选择要写入的列
    mode='w'  # 写入模式（'w'覆盖,'a'追加）
)

# 输出的文件中name前有一个“,”
# 前面的逗号 = Pandas 默认输出了行索引列，没有名字，所以开头空一格 + 逗号

print("写入CSV文件（指定参数）:")
print("文件已保存到output_with_params.csv")
print_dot()

# 处理特殊格式的CSV
# 有时CSV文件可能使用不同的分隔符（如制表符）或有特殊格式
# 读取TSV（制表符分隔）文件
df_tsv = pd.read_csv('data.tsv', sep='\t')
print("读取TSV文件:")
print(df_tsv.head())
# 读取以分号分隔的CSV文件
df_semicolon = pd.read_csv('data2.csv', sep=';')
print("读取分号分隔的CSV文件:")
print(df_semicolon.head())
print_star()

# 4.2 Excel 文件的读取与写入
# Excel 文件是另一种常见的数据格式,Pandas 通过openpyxl或xlrd库支持 Excel 文件操作
# 读取 Excel 文件 使用pd.read_excel() 函数读取 Excel 文件
# 读取Excel文件（最简单方式）
df_excel = pd.read_excel('data.xlsx')
print("读取Excel文件（默认参数）:")
print(df_excel.head())
# 读取Excel文件并指定参数
df_excel_params = pd.read_excel(
    'data.xlsx',
    sheet_name='Sheet1',  # 指定工作表（可以是名称或索引）
    header=0,  # 指定哪一行作为列名
    index_col=None,  # 指定索引列
    # usecols=['Date', 'Name', 'Age', 'Score', 'City'],  # 指定读取哪些列
    nrows=None,  # 读取的行数
    na_values=['NA', 'N/A'],  # 识别为缺失值的字符串
    parse_dates=['Date'],  # 将指定列解析为日期
    engine='openpyxl'  # 使用的引擎（openpyxl或xlrd）
)
print("读取Excel文件（指定参数）:")
print(df_excel_params.info())
print_dot()

# 写入 Excel 文件
# 使用DataFrame.to_excel() 方法写入 Excel 文件
# 写入Excel文件（最简单方式）
df_to_excel = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'Score': [85.5, 90.0, 78.5, 88.0],
    'City': ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen']
})
# 写入Excel文件
df_to_excel.to_excel('output.xlsx', sheet_name='Sheet1', index=False)
print("写入Excel文件（默认参数）:")
print("文件已保存到output.xlsx")
# 写入Excel文件并指定参数
df_to_excel.to_excel(
    'output_with_params.xlsx',
    sheet_name='Data',  # 工作表名称
    na_rep='N/A',  # 缺失值的表示方式
    float_format='%.1f',  # 浮点数格式
    index=True,  # 是否包含索引
    header=True,  # 是否包含列名
    columns=['Name', 'Age', 'City'],  # 选择要写入的列
    engine='openpyxl'  # 使用的引擎
)
print("写入Excel文件（指定参数）:")
print("文件已保存到output_with_params.xlsx")
print_dot()

# 读取多个工作表
# 读取Excel文件中的所有工作表
xl = pd.ExcelFile('data.xlsx')
print("Excel文件中的工作表:")
print(xl.sheet_names)
# 读取所有工作表到字典
dfs = {}
for sheet_name in xl.sheet_names:
    dfs[sheet_name] = xl.parse(sheet_name)
    print("读取所有工作表:")
for sheet_name, df in dfs.items():
    print(f"{sheet_name}工作表:")
    # 表头（列名）:Name, Age, City → 不算行
    # 第一行数据:索引 0 → 算行，会被 head () 包含
    print(df.head())
print_star()

# 4.3 其他数据格式的支持
# Pandas 还支持多种其他数据格式
# JSON 格式
# 读取JSON文件
df_json = pd.read_json('data.json')
print("读取JSON文件:")
print_dot()

print(df_json.head())
# 写入JSON文件
df_to_json = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40]
})
df_to_json.to_json('output.json', orient='records')
print("写入JSON文件:")
print("文件已保存到output.json")
print_star()

# Parquet 格式（列式存储）
# 读取Parquet文件（需要安装pyarrow或fastparquet）
df_parquet = pd.read_parquet('output.parquet')
print("读取Parquet文件:")
print(df_parquet.head())
# 写入Parquet文件
df_to_parquet = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Score': [85.5, 90.0, 78.5, 88.0]
})
df_to_parquet.to_parquet('output.parquet')
print("写入Parquet文件:")
print("文件已保存到output.parquet")

# 现在还用不上，教程里面有，一起了解一下，先不运行，看完改好以后
# 数据库查询结果
# Pandas 可以直接从数据库读取数据
# import sqlite3
# # 连接到SQLite数据库
# conn = sqlite3.connect('mydatabase.db')
# # 执行SQL查询
# query = "SELECT * FROM employees WHERE department = 'Sales'"
# df_sql = pd.read_sql(query, conn)
# print("从数据库读取数据:")
# print(df_sql.head())
# # 关闭数据库连接
# conn.close()
print_star()

# 5. 数据清洗
# 一、数据读取与导入
# 1.1 CSV 文件读取
# 在数据清洗工作中，CSV（逗号分隔值）是最常见的数据格式之一
# Pandas 提供了强大的read_csv函数来读取 CSV 文件
# 其语法如下:
# pd.read_csv(filepath_or_buffer, sep=',', header='infer', names=None, index_col=None, usecols=None, dtype=None,
#             engine=None, ...)
# 其中filepath_or_buffer是必需参数，指定要读取的文件路径或 URL
# sep参数用于指定分隔符，默认为逗号 ','
# 在实际应用中，经常会遇到中文编码问题 Pandas 默认采用 UTF - 8 编码读取文件
# 而许多中文系统导出的 CSV 文件实际使用的是 GBK 或 GB2312 编码，导致解码失败
# 解决方法是在读取时显式指定encoding = 'gbk' 或encoding = 'cp936'
# 对于带 BOM 的 UTF - 8 文件，可以使用encoding = 'utf-8-sig' 参数
# 以下是一个完整的
# CSV
# 读取示例:

# 读取CSV文件
df = pd.read_csv('Data_File/sales_data.csv',
                 sep=',',
                 header=0,
                 names=['日期', '地区', '销售额', '销量'],
                 dtype={'日期': 'str', '地区': 'category', '销售额': 'float64', '销量': 'int32'})
print("数据形状:", df.shape)
print("数据类型:")
print(df.dtypes)
print_dot()

# 1.2 Excel 文件读取
# Excel 文件的读取使用read_excel函数，该函数支持多种 Excel 文件格式，包括 xls、xlsx、xlsm、xlsb、odf、ods 和 odt
# pd.read_excel(io, sheet_name=0, header=0, names=None, index_col=None, usecols=None, dtype=None, engine=None, ...)
# 其中io是必需参数，指定 Excel 文件的路径或文件对象
# sheet_name参数可以是字符串（工作表名称）、整数（0 索引的位置）、列表（多个工作表）或None（所有工作表）
# 当 Excel 文件包含多个工作表时，可以通过以下方式读取
# 读取所有工作表，返回字典
all_sheets = pd.read_excel('Data_File/sales_report.xlsx', sheet_name=None)
# 读取指定的多个工作表
sheets_needed = pd.read_excel('Data_File/sales_report.xlsx', sheet_name=['Sheet1', 'Sheet2'])
# 读取第二个工作表
df_sheet2 = pd.read_excel('Data_File/sales_report.xlsx', sheet_name=1)
print(all_sheets)
print_dot()
print(sheets_needed)
print_dot()
print(df_sheet2)
# 补充
# ✅ 读取 所有 表单 → 返回字典
# sheet_name=None
# ✅ 读取 指定多个 表单 → 返回字典
# sheet_name=["Sheet1", "销售数据"]
# ✅ 读取 单个 表单 → 返回 DataFrame
# sheet_name="Sheet1"
print_star()

# 1.3 JSON 文件读取
# JSON（JavaScript 对象表示法）是另一种常用的数据交换格式
# Pandas 的read_json函数支持多种 JSON 格式
# pd.read_json(path_or_buf, orient=None, typ='frame', dtype=None, convert_axes=None, convert_dates=True, ...)
# 其中orient参数指定 JSON 的结构方向，常用的包括
# - 'split':{index -> [index], columns -> [columns], data -> [values]}
# - 'records':[{column -> value}, ..., {column -> value}]（默认）
# - 'index':{index -> {column -> value}}
# - 'columns':{column -> {index -> value}}
# 对于大 JSON 文件，可以使用lines = True参数逐行读取
# 逐行读取大JSON文件
df = pd.read_json('Data_File/large_data.json', lines=True, chunksize=10000)
# 处理每个数据块
for chunk in df:
    # 处理代码
    pass
print_star()

# 1.4 Parquet 文件读取
# Parquet 是一种列式存储格式，具有高效的压缩和快速查询特性
# Pandas 通过read_parquet函数支持 Parquet
# 文件读取:
# pd.read_parquet(path, engine='auto', columns=None, storage_options=None, ...)
# 其中engine参数可以是 'auto'（默认）、'pyarrow' 或 'fastparquet'
# 建议使用 'pyarrow' 引擎，因为它支持更多功能且性能更好

# 使用pyarrow引擎读取Parquet文件
# df = pd.read_parquet('data.parquet', engine='pyarrow')

# 只读取指定列
# df_selected = pd.read_parquet('data.parquet', columns=['id', 'name', 'age'])
print_star()

# 1.5 数据类型推断与指定
# 数据类型的正确识别对后续清洗工作至关重要
# Pandas 在读取数据时会自动推断数据类型，但在以下情况下需要显式指定

# 混合类型列:当列中包含多种数据类型时，Pandas 会将其推断为object类型
# 例如，包含数字和字符串的列:
# 显式指定数据类型
df1 = pd.read_csv('Data_File/data.csv', dtype={'id': 'str', 'value': 'float64'})
# 大整数 ID:对于超过 64 位整数范围的 ID（如 18 位身份证号），应指定为字符串类型:
df2 = pd.read_csv('Data_File/users.csv', dtype={'user_id': 'string'})
# 日期时间列:虽然 Pandas 可以自动识别部分日期格式，但显式指定可以提高解析速度:
df3 = pd.read_csv('Data_File/transactions.csv',
                  parse_dates=['transaction_date'],
                  dtype={'amount': 'float32'})
print(df1)
print(df2)
print(df3)

# 二、数据质量检查
# 2.1 缺失值识别
# 缺失值是数据清洗中最常见的问题之一
# Pandas 提供了多种方法来识别缺失值:
# - isna() / isnull():检测缺失值，返回布尔型对象(94)
# - notna() / notnull():检测非缺失值，返回布尔型对象(94)
# - isna().sum():统计每列缺失值数量
# - isna().sum() / len(df) * 100:计算缺失值百分比
# 检测缺失值
df = pd.read_csv("Data_File/pandas_data_cleaning_advanced.csv")
print("缺失值检测:")
print(df.isna())
# 统计各列缺失值数量
missing_values = df.isna().sum()
print_dot()
print("各列缺失值数量:")
print(missing_values)
print_dot()
# 计算缺失值百分比

# len(df) 在 Pandas 中返回 DataFrame 的行数（记录数），等价于 df.shape[0]
# df.isna().sum() 用于统计 DataFrame 每列的缺失值数量
# 返回一个 pandas.Series 类型。
# 索引：原 DataFrame 的列名
# 值：每列缺失值的数量（int64）
# dtype：int64
# 如果指定 axis=1，即 df.isna().sum(axis=1)，则返回每行缺失值数量的 Series，索引为原行索引

# 补充
# 遍历 DataFrame 时优先用 df.iterrows() 或 df.itertuples()，而非 range(len(df))，后者效率较低
# df.iterrows() 和 df.itertuples() 都是 Pandas 中逐行遍历 DataFrame 的方法，但性能和返回格式有显著差异

# 1. df.iterrows() — 逐行返回 (索引, Series)
# for index, row in df.iterrows():
#     print(index, row['姓名'], row['年龄'])
# 特点	    说明
# 返回	    (索引, Series) 元组
# 数据类型	数值列会被转为 float64（因为 Series 需要统一类型），可能丢失原始类型
# 速度	    慢，每次迭代都创建 Series 对象
# 适用	    需要按列名访问、数据量较小（<1万行）
# ⚠️ 注意：修改 row 不会反映到原 DataFrame，需用 df.loc[index, '列名'] = 值

# 2. df.itertuples() — 逐行返回命名元组
# for row in df.itertuples():
#     print(row.姓名, row.年龄)
#     # 或 print(row[1], row[2])  # 按位置访问
# 特点	    说明
# 返回	    Pandas(Index=..., 列1=..., 列2=...) 命名元组
# 数据类型	保留原始数据类型，不会强制转换
# 速度	    快，比 iterrows() 快约 10~100 倍
# 适用	    大数据量遍历、只读操作、性能敏感场景
# 列名含空格或特殊字符时，可用 getattr(row, '列 名') 或 row._1（按位置）
# 1. getattr(row, '列名') — 用字符串指定属性名
# '员工 姓名': ['张三', '李四']
# name = getattr(row, '员工 姓名')
# 2. row._1、row._2 — 按位置索引访问
# itertuples() 自动给每个字段分配位置编号：
# row.Index 或 row._0 → 行索引
# row._1 → 第 1 列
# for row in df.itertuples():
#     print(row._0)   # 行索引，等价于 row.Index
#     print(row._1)   # 第1列：员工 姓名
#     print(row._2)   # 第2列：基本工资(元)
#     print(row._3)   # 第3列：绩效评分
# ⚠️ 注意：_1 对应的是 DataFrame 的第 1 列（从 1 开始计数），不是 Python 常规的 0 开始索引。_0 固定留给行索引

missing_percentage = (df.isna().sum() / len(df)) * 100
print("缺失值百分比:")
print(missing_percentage)
print_star()

# 2.2 重复值识别
# 重复值会影响分析结果的准确性
# Pandas 的 duplicated方法可以标记重复行:
# DataFrame.duplicated(subset=None, keep='first', inplace=False)
# 其中subset指定要检查的列，keep参数指定保留策略:
# - 'first':保留第一个出现的行（默认）
# - 'last':保留最后一个出现的行
# - False:标记所有重复行(104)
# 检测所有列的重复值
print("检测所有行的重复值:")
print(df)
# df.duplicated() 用于检测 DataFrame 中的重复行，返回一个布尔型 Series
duplicates = df.duplicated()
print(duplicates)
# 检测特定列的重复值
print("检测ID列的重复值:")
# 不算 id 本身
id_duplicates = df.duplicated(subset=['id'])
print(id_duplicates)
# 统计重复行数
print(f"重复行数量:{id_duplicates.sum()}")
print_star()


# 2.3 异常值检测
# 异常值是指明显偏离正常范围的数据点
# 常用的检测方法包括:
# 1. 描述性统计法:使用describe()
# 方法查看数据的基本统计信息，识别异常值
# 2. 四分位距（IQR）法
# - 计算第一四分位数（Q1）和第三四分位数（Q3）
# - 计算四分位距:IQR = Q3 - Q1
# - 定义异常值范围:小于 Q1 - 1.5 * IQR 或大于 Q3 + 1.5 * IQR
def detect_outliers_iqr(series):
    """使用IQR方法检测异常值"""
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return series[(series < lower_bound) | (series > upper_bound)]


print_dot()

# 检测销售额列的异常值
# 这个函数返回的是一个 Series 子集，其索引（标签）完全继承自原始 series
# 特性	说明
# 类型	pandas.Series
# 索引	原 Series 的索引（行标签），保持不变
# 值	被判定为异常值的具体数值
# 长度	异常值的个数
outliers = detect_outliers_iqr(df['sales_amount'])
print(f"检测到{len(outliers)}个异常值:")
print(outliers)
# 3. Z-Score 法:计算数据点与均值的标准差倍数，通常绝对值大于 3 的被视为异常值
print_star()

# 2.4 数据类型检查
# 数据类型错误会导致计算错误或内存浪费。使用以下方法检查数据类型:
# - dtypes属性:查看各列的数据类型
# - info()方法:查看数据结构、数据类型、非空值数量和内存使用情况
# 查看数据类型
print("数据类型:")
print(df.dtypes)
print_dot()

# 查看详细信息
print("数据结构信息:")
df.info()
print_dot()
# 举例说明
# 0   id            254 non-null    str
# 列序号0，列名id，有 254 个非空值，数据类型str
# 注意：入职日期 目前是 str（文本），如果需要按时间分析（如计算工龄），后续可能需要转换为日期格式。

# 检查是否有混合类型列
# 此处生成的数据没有
print("检查混合类型:")
for col in df.columns:
    if df[col].dtype == 'object':
        unique_types = set(type(x) for x in df[col].dropna())
        if len(unique_types) > 1:
            print(f"{col}列包含混合类型:{unique_types}")
print_star()
# 输出
# 检查混合类型:
# **************************************************


# 2.5 数据完整性检查
# 数据完整性检查包括:
# 1. 数据形状检查:使用shape属性查看数据的行数和列数
# 2. 非空值检查:使用info() 方法查看各列的非空值数量
# 3. 数值范围检查:检查数值是否在合理范围内
# 4. 逻辑一致性检查:检查相关列之间的逻辑关系
# 检查数据形状
print(f"数据形状:{df.shape}")
print(f"行数:{df.shape[0]}")
print(f"列数:{df.shape[1]}")
print_dot()

# 检查数值范围
print("数值范围检查:")
numeric_cols = df.select_dtypes(include=['int', 'float']).columns
for col in numeric_cols:
    min_val = df[col].min()
    max_val = df[col].max()
    print(f"{col}:最小值{min_val}，最大值{max_val}")
# 逻辑检查示例:入职日期不能晚于当前日期
print("逻辑检查:")
print_dot()

# 1. 确保列是日期格式
# pd.to_datetime(...)：这是 Pandas 处理日期的核心函数。它会把列中的文本（如 "2023-01-01"）转换成真正的日期对象
# errors='coerce'：这是一个保险措施。如果你的数据里混有 "未知"、"2099-99-99" 这种无法识别的日期，加上这个参数会让 Pandas 把它们变成“缺失值”（NaT），而不是直接让程序崩溃报错。
# 类型匹配：转换后，对象可以进行大小比较
df['hire_date'] = pd.to_datetime(df['hire_date'], errors='coerce')

# 2. 获取当前日期，并转换为字符串格式
# Pandas 的日期时间类型不能直接与 Python 原生的 datetime.date 对象进行比较
# 使用 isoformat() 得到 'YYYY-MM-DD' 格式，这是 Pandas 最喜欢的标准格式
current_date = datetime.date.today().isoformat()

# datetime.date.today().isoformat()：这会生成类似 '2026-04-27' 的字符串
# Pandas 的智能比较：当你用字符串（如 '2026-04-27'）去比较 datetime64 列时
# Pandas 会自动把这个字符串当作时间点来处理，从而避免了类型不匹配的错误
invalid_dates = df[df['hire_date'] > current_date]
print(f"发现{len(invalid_dates)}条入职日期晚于当前日期的记录")
print_star()

# 三、核心清洗操作
# 3.1 缺失值处理
# 3.1.1 删除缺失值
# 删除缺失值是处理缺失数据最直接的方法，适用于缺失率较低的情况（通常低于5 %）
# Pandas 提供了dropna方法来删除缺失值:
# DataFrame.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)
# 参数说明:
# - axis:0 表示删除行，1 表示删除列
# - how:'any' 表示只要有缺失值就删除，'all' 表示所有值都缺失才删除
# - thresh:保留至少有thresh个非缺失值的行 / 列
# - subset:指定检查的列子集

# 删除所有包含缺失值的行
df_cleaned = df.dropna()
print(df_cleaned)
print_dot()
# 删除所有值都缺失的行
df_cleaned = df.dropna(how='all')
print(df_cleaned)
print_dot()
# 只删除特定列有缺失值的行
df_cleaned = df.dropna(subset=['name', 'tel', '交通补贴'])
print(df_cleaned)
print_dot()
# 保留至少有3个非缺失值的行, 要将测试数据删除到3个一下，才会删除，暂时不删了，了解函数功能即可
df_cleaned = df.dropna(thresh=3)
print(df_cleaned)
print_star()

# 3.1.2 填充缺失值
# 当缺失率较高或删除会损失重要信息时，可以使用填充方法
# Pandas 的 fillna 方法提供了多种填充策略:
# DataFrame.fillna(value=None, method=None, axis=None, inplace=False, limit=None, downcast=None)
# 常用的填充方法:
# 1. 常数填充:使用固定值填充，如0、"未知"等
# 2. 前向填充（ffill）:使用前面的有效值填充
# 3. 后向填充（bfill）:使用后面的有效值填充
# 4. 统计值填充:使用均值、中位数、众数等填充

print("原数据：")
print(df)
# 用0填充数值型缺失值
df['age'] = df['age'].fillna(0)
# 用"未知"填充字符串型缺失值
df['address'] = df['address'].fillna('未知')
# 前向填充
df['salary'] = df['salary'].ffill()
# 后向填充
df['salary'] = df['salary'].bfill()
# 用均值填充
df['age'] = df['age'].fillna(df['age'].mean())
# 用中位数填充
df['income'] = df['income'].fillna(df['income'].median())
# 用众数填充分类变量
df['category'] = df['category'].fillna(df['category'].mode()[0])
print("填充后：")
print(df)
print_star()
# 运行结果应该是正确的，编辑器输出不能预览全部，改了几条数据，结算是对的


# 3.1.3 插值法填充
# 对于连续型数据，可以使用插值法更精确地估算缺失值
# Pandas 的 interpolate 方法支持多种插值方法:
# DataFrame.interpolate(method='linear', axis=0, limit=None, inplace=False, limit_direction=None, ...)
# 常用方法:
# - 'linear':线性插值（默认）
# - 'time':时间序列插值
# - 'quadratic':二次多项式插值
# - 'cubic':三次样条插值
# 核心目的都是“估算并填充缺失的数据”，但根据数据特性和业务需求，采用不同的算法和限制条件

# 线性插值
# 含义：这是 interpolate() 的默认模式（method='linear'）。它假设数据的变化是直线的
# 原理：它会根据缺失值前后两个最近的已知数据点，画一条直线，计算中间点的数值
# 适用场景：气温、身高、体重等变化相对平滑、连续的数据
# 例子：
# 周一 20度，周三 24度。
# 周二的缺失值会被填为 22度（20和24的中间值）
df['temperature'] = df['temperature'].interpolate()

# 时间序列插值 (销售)
# 含义：指定 method='time'。这不仅看数据的顺序，还会考虑索引（时间）的具体间隔
# 原理：如果你的时间序列不是等间隔的（比如缺了周末，或者记录时间不固定），普通的线性插值会出错。这个模式会根据实际经过的时间长度来加权计算
# 适用场景：销售额、股票价格等时间序列数据，特别是当数据索引是日期时间类型，且可能存在非等间隔采样时
# 例子：
# 1月1日卖了100元，1月4日卖了400元（中间隔了3天）
# 1月2日的估算值会更靠近100，而不是简单的平均值
# 原始数据：时间间隔不均匀
data = {
    'time': ['2023-01-01 08:00', '2023-01-01 09:00', '2023-01-01 14:00', '2023-01-01 15:00'],
    'temp': [20.0, np.nan, np.nan, 26.0]
}
df_time = pd.DataFrame(data)
# 【关键步骤 1】：将 'time' 列转换为 datetime 对象
df_time['time'] = pd.to_datetime(df_time['time'])
# 【关键步骤 2】：将 'time' 列设为索引
df_time.set_index('time', inplace=True)
print("--- 设置时间索引后的数据 ---")
print(df_time)
# 【关键步骤 3】：指定 method='time'
# 这告诉 Pandas：请根据索引的时间差来计算权重，而不是简单的行号差
# 新建一列保存插值结果
# df_time['temp_interpolated'] = df_time['temp'].interpolate(method='time')
# 再缺失值的列插值
df_time['temp'] = df_time['temp'].interpolate(method='time')
print("\n--- 插值结果 ---")
print(df_time)
print_dot()

# 限制插值范围（最多连续填充3个缺失值）
# 含义：limit=3 是一个“安全阀”。它规定最多只能连续填充 3 个缺失值
# 原理：如果连续缺失的数据超过 3 个（比如连着缺了 5 个），interpolate 只会填补前 3 个，剩下的 2 个依然保持为 NaN
# 适用场景：当缺失数据过多时，插值的结果会变得非常不准确（纯属猜测，网上查的）。设置限制可以保留部分缺失值，提醒你这些数据不可靠
df['value'] = df['value'].interpolate(limit=3)
print(df)
print_dot()

# 仅填充被有效值包围的缺失值
# 含义：limit_direction='inside'（通常配合 limit_area='inside' 理解，但在代码语境中通常指只填充被有效数据“包围”的区域）
# 原理：
# Inside (内部)：如果缺失值在数据的中间（前后都有数据），则填充
# Outside (外部)：如果缺失值在数据的开头或结尾（前面没数据或后面没数据），则不填充
# 适用场景：你不想对数据的起始阶段或结束阶段进行“外推”预测，因为那通常比“内插”更危险、更不准确。你只想修补中间偶尔出现的断层

# 两个参数
# limit_direction：控制插值的方向（向前、向后、双向）。它的可选值只能是 'forward'、'backward' 或 'both'
# limit_area：控制插值的区域（只补中间、只补两头）。它的可选值才是 'inside'、'outside' 或 None
df['value'] = df['value'].interpolate(limit_area='inside')
print_star()

# 总结
# 代码特征	    核心逻辑	        形象比喻
# 默认 (线性)	两点之间连直线	    缺了一块砖，按直线补齐
# method='time'	按时间长短算斜率	考虑路程远近，计算平均速度
# limit=3	    缺太多就不补了	    补衣服：破洞小就补，破太大就不补了
# limit_direction='inside'	只补中间，不补两头	只修补中间断掉的链条，不延伸链条的首尾


# 3.2 重复值处理
# 处理重复值的完整流程包括:
# 1. 识别重复值:使用duplicated方法标记重复行
# 2. 查看重复数据:筛选出重复行进行分析
# 3. 删除重复值:使用drop_duplicates方法删除重复行
# 查看所有重复行（不包括首次出现）
duplicates_df = df[df.duplicated(keep=False)]
print(f"重复行数量:{len(duplicates_df)}")
print("重复行示例:")
print(duplicates_df.head())
# 删除重复行，保留第一个出现的
df_cleaned = df.drop_duplicates()
# 删除重复行，保留最后一个出现的
df_cleaned = df.drop_duplicates(keep='last')
# 基于特定列删除重复
df_cleaned = df.drop_duplicates(subset=['id'])
# 删除所有列都相同的重复行
df_cleaned = df.drop_duplicates(keep=False)
print_star()

# 3.3 数据类型转换
# 数据类型转换是数据清洗的重要环节，Pandas 提供了多种方法:
# 1. astype方法:强制转换数据类型(171)
# 2. to_numeric方法:智能转换为数值类型，可处理异常值(169)
# 3. to_datetime方法:转换为日期时间类型(195)

# 3.3.1
# 数值类型转换
# 使用to_numeric处理包含异常值的转换:
# 将字符串列转换为数值，错误值转换为NaN
# 是我需求描述不清，所以price是带符号的，大部分是会变成NaN的
df['price'] = pd.to_numeric(df['price'], errors='coerce')
# 转换并尝试向下转换以节省内存
df['quantity'] = pd.to_numeric(df['quantity'], downcast='integer')
# 转换为特定数值类型
df['age'] = df['age'].astype('int32')
df['weight'] = df['weight'].astype('float32')
print(df)
print_star()

# 3.3.2 字符串类型处理
# Pandas 的字符串方法提供了强大的文本处理能力:
# Series.str.strip(to_strip=None)  # 去除首尾空格或指定字符<reference type="end" id=185>
# Series.str.replace(pat, repl, n=-1, case=None, flags=0, regex=False)  # 替换字符串<reference type="end" id=184>
# Series.str.contains(pat, case=True, flags=0, na=False)  # 检查是否包含子串
# Series.str.extract(pat, flags=0, expand=True)  # 提取匹配的子串
# 去除字符串首尾空格
df['name'] = df['name'].str.strip()
# 替换特定字符
df['phone'] = df['phone'].str.replace('-', '')
# 删除所有非数字字符
df['phone'] = df['phone'].str.replace(r'D', '', regex=True)
# 转换为大写
df['category'] = df['category'].str.upper()
# 提取邮箱域名
df['email_domain'] = df['email'].str.extract('@([^@]+)$')
print(df)
print_star()

# 3.3.3
# 日期时间标准化
# 日期时间标准化是处理时间数据的关键:
# pd.to_datetime(arg, errors='raise', format=None, infer_datetime_format=False, ...)
# 转换日期字符串，错误值转换为NaT
df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
# 指定日期格式
df['birth_date'] = pd.to_datetime(df['birth_date'], format='mixed')
# 从多个列创建日期时间
df['datetime'] = pd.to_datetime(df[['year', 'month', 'day']])

# 转换时间戳（单位:秒）
# 你的数据是字符串日期 + 带时间 + 有无效值 → 绝对不能加 unit，必须加 errors='coerce'
# 会出现一个警告
# 因为数据格式很乱：1978/3/27、2015/8/30 19:16、invalid
# pandas 自动识别时会发出一个友好提醒，不是错误
# 加上 format='mixed' 就会关闭这个警告
df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed', errors='coerce')

# 仅转换特定列
df = df.convert_dtypes()
print(df)
print_star()

# 3.4 数据筛选与过滤
# 数据筛选是根据条件提取所需数据的过程:
# 1. 布尔索引:使用布尔表达式筛选数据
# 2. query方法:使用字符串表达式进行查询
# 3. loc方法:基于标签筛选
# 4. iloc方法:基于位置筛选
# 布尔索引示例
# 筛选年龄在25-40岁之间的数据
df_filtered = df[(df['age'] >= 25) & (df['age'] <= 40)]
print(df_filtered)
print_dot()
# 筛选收入大于10000或...
df_filtered = df[(df['income'] > 10000) | (df['category'] == '技术部')]
print(df_filtered)
print_dot()
# 筛选非空值记录
df_filtered = df[df['email'].notna()]
print(df_filtered)
print_dot()
# query方法示例
df_filtered = df.query('age >= 25 and age <= 40 and city == "北京"')
print(df_filtered)
print_dot()
# loc方法示例（基于标签）
# 筛选id为100到150的记录，包含name和age列
df_filtered = df.loc[100:150, ['name', 'age']]
print(df_filtered)
print_dot()
# iloc方法示例（基于位置）
# 筛选前10行，第2到第4列
df_filtered = df.iloc[:10, 1:4]
print(df_filtered)
print_star()

# 四、高级清洗技术
# 4.1 分组清洗
# 分组清洗是指按类别对数据进行分组，然后对每个组内的数据进行清洗。这种方法特别适用于需要按类别处理缺失值或异常值的场景。

df2 = pd.read_csv("File_Generation/data_clean_demo.csv")
print("原数据: ")
print(df2)
print_dot()

# 按部门分组，用各组的均值填充缺失的工资
df2['salary'] = df2.groupby('department')['salary'].transform(lambda x: x.fillna(x.mean()))
# 按产品类别分组，用各组的中位数填充缺失值
df2['sales'] = df2.groupby('product_category')['sales'].transform(lambda x: x.fillna(x.median()))
# 按地区分组，统计每组的缺失值数量
missing_by_group = df2.groupby('region')['value'].apply(lambda x: x.isna().sum())
print("清洗后: ")
print(df2)
print_dot()

print("各地区缺失值数量:")
print(missing_by_group)
# 按日期分组，删除每组中的重复记录
df_cleaned = df2.groupby('date').apply(lambda x: x.drop_duplicates())
print_star()

# 4.2
# 条件清洗
# 条件清洗是根据特定条件对数据进行选择性清洗:
# 条件清洗示例
# 1. 将工资低于0的值设为0（处理负值）
df2['salary'] = df2['salary'].where(df2['salary'] > 0, 0)
# 2. 将年龄超过100岁的值设为100（封顶处理）
df2['age'] = df2['age'].where(df2['age'] <= 100, 100)
# 3. 根据条件填充缺失值
# 如果收入缺失且职业是教师，用教师的平均收入填充,数据里面没有
# df2['income'] = df2['income'].fillna(
#     df2.groupby('job')['income'].transform('mean')
# )
# 4. 批量条件替换
conditions = [
    (df2['score'] >= 90),
    (df2['score'] >= 80),
    (df2['score'] >= 70),
    (df2['score'] >= 60)
]
choices = ['A', 'B', 'C', 'D']
df2['grade'] = np.select(conditions, choices, default='E')
print(df2)
print_star()


# 5. 复杂条件清洗（使用apply）
def clean_data(row):
    """复杂的单行数据清洗函数"""
    # 清洗姓名
    row['name'] = row['name'].strip().title()

    # 清洗邮箱
    email = row['email']
    if not isinstance(email, str) or '@' not in email:
        row['email'] = None
        return False  # 示例

    # 清洗年龄（限制在18-100岁）
    if row['age'] < 18 or row['age'] > 100:
        row['age'] = None
    return row


df_cleaned = df2.apply(clean_data, axis=1)
print_star()


# 4.3
# 数据标准化与归一化
# 数据标准化与归一化是将数据转换为统一尺度的过程，常用于机器学习预处理:
# 4.3.1
# Min - Max 归一化
# 将数据缩放到[0, 1]区间:
def min_max_normalization(x):
    """Min-Max归一化"""
    return (x - x.min()) / (x.max() - x.min())


print("原数据")
print(df2)
# 对数值列进行Min-Max归一化
numeric_cols = df2.select_dtypes(include=['int', 'float']).columns
df2_normalized = df2[numeric_cols].apply(min_max_normalization)


# 缩放到指定区间（如0-100）
def scaled_min_max(x, min_val=0, max_val=100):
    return min_val + (x - x.min()) * (max_val - min_val) / (x.max() - x.min())


df2['scaled_score'] = scaled_min_max(df2['score'], 0, 100)
print(df2)
print_star()


# 4.3.2 Z-Score 标准化
# 将数据转换成 均值为0，标准差为1
# 的标准正态分布:
def z_score_standardization(x):
    """Z-Score标准化"""
    return (x - x.mean()) / x.std()


# 加载数据
# df = pd.read_csv("File_Generation/numeric.csv")
# 对数值列进行Z-Score标准化
df_standardized = df2[numeric_cols].apply(z_score_standardization)


# .apply()
# 作用 对 Series / DataFrame 的行或列，批量执行自定义函数
# 语法
# # Series
# series.apply(func)
# # DataFrame
# df.apply(func, axis=0)  # axis=0：默认 按列
# df.apply(func, axis=1)  # axis=1：按行


# 处理包含异常值的情况（使用稳健统计量）
def robust_standardization(x):
    """使用中位数和四分位距进行稳健标准化"""
    q1 = x.quantile(0.25)
    q3 = x.quantile(0.75)
    iqr = q3 - q1
    return (x - x.median()) / iqr


df_robust = df2[numeric_cols].apply(robust_standardization)
print(df_robust)
print_star()

# 4.4 文本数据特殊清洗
# 文本数据清洗是数据清洗中最复杂的部分之一，需要处理各种不规则的文本格式:
# 1. 文本标准化:统一文本格式（如统一为小写、去除多余空格）
# 2. 停用词处理:去除无意义的词汇（如"的"、"了"等）
# 3. 词干提取与词形还原:将词汇转换为基本形式
# 4. 特殊字符处理:处理标点符号、表情符号等
# 5. 语言检测与转换:检测文本语言并进行转换
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

# # 初始化工具
# stop_words = set(stopwords.words('english'))  # 英文停用词（the/a/is/and...无意义词）
# stemmer = PorterStemmer()  # 词干提取器（running → run）
# lemmatizer = WordNetLemmatizer()  # 词形还原器（better → good）
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
#
#
# def clean_text(text):
#     """完整的文本清洗函数"""
#     # 处理缺失值，避免报错
#     if pd.isna(text):
#         return None
#
#     # 1. 转换为小写
#     text = text.lower()
#     # 2. 去除URL
#     # re.sub()：替换函数（regular expression substitute）
#     # 作用: 在字符串里查找符合规则的内容 → 替换成别的内容
#     # 规则: r'http\S+'
#     # http: 匹配以 http 开头的网址
#     # \S+: 匹配所有非空格字符（一直到空格为止）
#     text = re.sub(r'http\S+', '', text)
#     # 3. 去除特殊字符和数字
#     # 删除数字、标点、符号、表情，只留下字母和空格
#     # [^a-zA-Z\s]是反向匹配
#     #  a-z: 小写字母
#     #  A-Z: 大写字母
#     #  \s: 空格
#     #  ^: 除了…之外
#     #  把不是字母、不是空格的东西全部删掉, 只保留英文，删除乱七八糟的符号和数字
#     text = re.sub(r'[^a-zA-Zs]', '', text)
#     # 4. 去除多余空格
#     # \s+: 匹配1个或多个连续空格
#     # 替换成' ': 1个空格
#     # .strip(): 删除句子开头和结尾的空格
#     text = re.sub(r's+', ' ', text).strip()
#     # 5. 去除停用词
#     # 删除the/a/an/is/are/and/of等没用的词
#     # text.split()：把句子按空格切成单词列表
#     # if word not in stop_words：只保留不是停用词的单词
#     print("原数据: " + text)
#     words = text.split()
#     print("分割后: " + text)
#     words = [word for word in words if word not in stop_words]
#     # 6. 词干提取
#     # 把变化形式的单词，统一成最短词根
#     # 统一单词形态，减少词汇数量
#     words = [stemmer.stem(word) for word in words]
#     # 7. 词形还原
#     # 根据语法把单词还原成原始形态
#     # 比词干提取更准确：
#     # better → good
#     # drove → drive
#     # women → woman
#     # ate → eat
#     # 总结
#     # 让单词回归字典里的原型
#     words = [lemmatizer.lemmatize(word) for word in words]
#     return ' '.join(words)
#
#
# data = {
#     'raw_text': [
#         "I love running! It's 100% fun, check http://sport.com",
#         "The cats are playing in the garden!!!",
#         "This is a very good movie, I liked it a lot!!!",
#         "Hello WORLD!!! Today is 2025-01-01",
#         None,  # 空值测试
#         "Better late than never!!! 12345",
#         "I am learning Python and Data Science very happily",
#         "   Too   many   spaces   here   "
#     ]
# }
#
# df = pd.DataFrame(data)
# df['cleaned_text'] = df['raw_text'].apply(clean_text)

# \s = 1 个空格
# + = 至少 1 个，越多越好
# \s+ = 一段连续空格（不管多少个）

# re.sub(r'http\S+', '', text) → 删网址
# re.sub(r'[^a-zA-Z\s]', '', text) → 只留英文
# re.sub(r'\s+', ' ', text).strip() → 清理空格
# if word not in stop_words → 删无用虚词
# stemmer.stem() → 粗暴词根化
# lemmatizer.lemmatize() → 智能还原单词

# print(df)

# 对文本列应用清洗函数
# df['cleaned_text'] = df['raw_text'].apply(clean_text)
# print()
##################################################################################


# 五、实践练习 5.1
# 单表清洗练习
# 5.1.1
# 练习一:电商订单数据清洗
# 数据描述:
# - 数据来源:某电商平台订单数据
# - 文件格式:CSV
# - 包含字段:订单ID、用户ID、商品名称、价格、数量、下单时间、支付状态、收货地址
# - 数据问题:包含缺失值、重复订单、价格异常、日期格式不一致
# 清洗要求:
# 1. 读取数据并检查数据质量
# 2. 处理缺失值（订单ID、用户ID不得缺失）
# 3. 删除重复订单
# 4. 修复价格异常（负值、超大值）
# 5 标准化日期格式
# 6.清洗收货地址（只保留城市信息）

# 练习代码框架:
# 1. 读取数据
# 读取CSV文件（假设文件名为orders.csv）
df_orders = pd.read_csv('Data_File/orders.csv', encoding='utf-8')

# # 2. 数据质量检查
print("=== 订单数据质量检查 ===")
print("1. 数据基本信息:")
# 想知道表有多大，就用 .shape，先看行后看列 (11, 8) 11行8列，返回一个元组
print(f"数据形状:{df_orders.shape}")

# df_orders.info() 是 Pandas 中用于快速查看 DataFrame 内存摘要和数据质量的核心方法。
# 如果说 .shape 是看数据的“体型”，那么 .info() 就是给数据做一次全面的“体检”
# 在拿到任何一份新数据时，“标准起手式”通常是：
# df.head()：看前几行长什么样
# df.shape：看有多少行多少列
# df.info()：看有没有缺失值、看数据类型对不对
print(df_orders.info())

print("2. 缺失值检查:")
# 这行代码是 Pandas 里用来精准统计缺失值的“黄金组合”。它能把数据里隐藏的空值一个个揪出来，告诉你每一列到底缺了多少数据
# df_orders.isna()
# 1.作用：检查数据中的每一个单元格。
# 结果：返回一个和原表一样大的表格，但里面只有 True 和 False。
# 含义：True 代表这里是空的（缺失值），False 代表这里有数据。
# 2..sum()
# 作用：对上述的 True/False 表格进行求和。
# 原理：在 Python/Pandas 中，True 当作 1，False 当作 0。
# 默认行为：如果不指定轴，它默认是按列求和（axis=0）。
# 3.最终结果
# 返回一个 Series 对象。
# 索引是列名，值是该列缺失值的总数量
missing_values = df_orders.isna().sum()
print(missing_values)

print("3. 重复值检查:")
# 1.df_orders.duplicated(subset=['order_id'])
# 作用：检查 order_id 列的值是否重复。
# 参数 subset=['order_id']：告诉 Pandas 只关注 order_id 这一列。只要订单号一样，就算重复，不管其他列（如价格、时间）是否一样。
# 返回值：返回一个布尔序列（True/False）。
# False：表示这是该订单号第一次出现（保留项）。
# True：表示这个订单号之前已经出现过了（重复项）。
# 2..sum()
# 作用：对布尔值求和。
# 原理：在计算中，True 视为 1，False 视为 0。
# 结果：算出总共有多少个被标记为 True 的行。
print(f"重复订单数量:{df_orders.duplicated(subset=['order_id']).sum()}")

print("4. 价格范围检查:")
# 这个我自己能看懂，还是查了一下
# 先拿到列，再求最值
# 索引方式	代码示例	    返回类型	    形象理解
# 单括号	    df['Age']	Series	    把这一列抽出来，变成一维数组
# 双括号	    df[['Age']]	DataFrame	把这一列框选住，它还是个表格（只是只有一列）
# :.2f 是格式化字符串的语法
print(f"价格最小值:{df_orders['price'].min():.2f}")
print(f"价格最大值:{df_orders['price'].max():.2f}")

# 3. 数据清洗
print("=== 开始数据清洗 ===")
# 处理缺失值
print("1. 处理缺失值:")
# 删除订单ID或用户ID缺失的记录
print(f"原记录数:{len(df_orders)}")
# 数据中user_id有一行为空
df_orders_clean = df_orders.dropna(subset=['order_id', 'user_id'])
print(f"删除缺失值后剩余记录数:{len(df_orders_clean)}")
# 用0填充数量缺失值（假设缺失表示0个）
df_orders_clean.loc[:, 'quantity'] = df_orders_clean['quantity'].fillna(0)
# 用均值填充价格缺失值（不推荐，仅示例）
df_orders_clean.loc[:, 'price'] = df_orders_clean['price'].fillna(df_orders_clean['price'].mean())
# 处理重复订单
print("2. 处理重复订单:")
# 保留最新的订单（假设order_id唯一，但可能有重复）
# order_id一条重复

'''
df.drop_duplicates(subset=None, keep='first', inplace=False, ignore_index=False)
是 Pandas 中用于数据去重的核心函数。简单来说，它的作用就是帮你在 DataFrame 中找出重复的行，并根据你的要求保留或剔除它们，确保数据的唯一性
1. subset：按哪一列（或哪些列）去重？
默认值：None。
含义：
      None：检查所有列。只有当一行数据的所有内容都与另一行完全一样时，才算重复。
      ['列名']：只检查指定的列。只要这一列的值相同，不管其他列是什么，都算重复。
场景：比如你想根据“用户ID”去重，就设置 subset=['用户ID']。
2. keep：保留哪一个？
这是控制去重策略的关键参数，有三个选项：
      'first' (默认)：“喜新厌旧”的反义词。保留第一次出现的行，删除后面重复的行。
      'last'：“喜新厌旧”。保留最后一次出现的行，删除前面重复的行。常用于保留最新状态的订单。
      False：“六亲不认”。不保留任何重复项，把所有重复的行（包括第一次和最后一次）统统删除。只留下那些在表中独一无二的行。
3. inplace：是否修改原数据？
      False (默认)：不修改原 DataFrame，而是返回一个新的去重后的 DataFrame。
      True：直接在原 DataFrame 上修改，不返回新对象。
4. ignore_index：是否重置索引？
      False (默认)：保留原来的行号（索引）。去重后索引可能会断断续续（如 0, 2, 5...）。
      True：去重后，将索引重置为连续的 0, 1, 2...。
'''

df_orders_clean = df_orders_clean.drop_duplicates(subset=['order_id'], keep='last')
print(f"删除重复订单后剩余记录数:{len(df_orders_clean)}")
# 处理价格异常
print("3. 处理价格异常:")

# 找出价格小于0的记录
negative_price = df_orders_clean[df_orders_clean['price'] < 0]
'''
1.df_orders_clean['price'] < 0
这行代码本身会返回一个 Series，里面的数据全是 True 或者 False
Pandas 会逐行检查 price 列
2.df_orders_clean[...]
这是布尔索引
Pandas 拿着上面那串 True/False 序列去套在原表上
只保留对应位置是 True 的行，丢弃 False 的行

其实我是知道一些的，理解也之前，下面的表述要更正式
方括号 [] 中放入一个 布尔类型的 Series（即由 True/False 组成的序列）时，Pandas 会将其视为一个掩码（Mask）或筛选器，对原 DataFrame 进行行过滤
输入：df_orders_clean['price'] < 0 生成了一个布尔 Series。
这个 Series 的长度与原表行数一致。
每个 True 代表“保留这一行”，每个 False 代表“丢弃这一行”。
执行：df_orders_clean[...] 接收这个 Series。
Pandas 会逐行比对，只把对应位置为 True 的行提取出来。
输出：结果依然是一个 DataFrame。
结构不变：列名、列的数据类型都保持不变。
行数减少：只包含满足条件的行。
索引保持：默认情况下，保留原表的行索引（除非你后续重置它）。

为什么是 DataFrame？
因为筛选操作只是减少了行的数量，并没有改变数据的二维表格结构
你得到的仍然是一个包含多列数据（订单ID、商品、价格等）的集合，所以它必须是 DataFrame
'''

print(f"发现{len(negative_price)}条负价格记录")

# 找出价格超过10000的记录（假设正常价格不超过10000）
high_price = df_orders_clean[df_orders_clean['price'] > 10000]
print(f"发现{len(high_price)}条超高价格记录")
'''
将异常价格设为NaN（后续处理）
.where(..., np.nan)（执行替换）
语法：df.where(条件, 替换值)
含义：
    如果条件是 True（价格正常）：保留原来的价格数字。
    如果条件是 False（价格异常）：将该位置的值替换为 np.nan（空值）
这里再修改以后写回数据，数据改变
'''
df_orders_clean['price'] = df_orders_clean['price'].where(
    (df_orders_clean['price'] >= 0) & (df_orders_clean['price'] <= 10000),
    np.nan
)

# 用中位数填充异常价格
df_orders_clean['price'] = df_orders_clean['price'].fillna(df_orders_clean['price'].median())

# 标准化日期格式
print("4. 标准化日期格式:")
# 第一行负责“标准化”（把杂乱的文本变成标准时间）
# 第二行负责“截取”（只要日期，不要具体几点几分）
print("原始日期格式示例:", df_orders_clean['order_time'].iloc[0])
# 转换为datetime类型
df_orders_clean['order_time'] = pd.to_datetime(df_orders_clean['order_time'], errors='coerce')
"""
作用：将 order_time 列从“文本字符串”转换为 Pandas 的“标准时间戳”格式。
pd.to_datetime(...)：
这是 Pandas 的强力转换器。它能识别各种格式的字符串（如 "2023/1/1 12:00"、"2023-01-01" 等），并将它们统一转换成 datetime64 类型。
转换后，这列数据就不再是普通的文字，而是计算机能理解的时间，可以进行计算（比如算时间差）。
errors='coerce'（关键点）：
这是一个“容错机制”。
如果不加这个参数，一旦数据里混进一个无法识别的格式（比如 "未知时间" 或 "2023-13-40"），整个程序就会报错崩溃。
加上 errors='coerce' 后，如果遇到无法转换的“脏数据”，Pandas 会把它变成 NaT，相当于时间领域的 NaN（空值）
这样程序能继续运行，你可以后续再处理这些空值。

只保留日期部分
作用：从标准时间中把“年月日”单独提取出来，存入新的一列 order_date。
.dt：
这是 Pandas 的“时间访问器”。只有当一列数据是标准时间格式时，才能使用 .dt。
.date：
这是一个属性，它的作用是“扔掉”时分秒，只保留日期部分。
注意：使用 .dt.date 提取后，该列的数据类型会变成 Python 原生的 datetime.date 对象（在 Pandas 中显示为 object 类型）。
"""
df_orders_clean['order_date'] = df_orders_clean['order_time'].dt.date
# 清洗收货地址
print("5. 清洗收货地址:")


# 从地址中提取城市信息（简化版）
def extract_city(address):
    """从地址中提取城市信息"""
    if pd.isna(address):
        return None
    # 简单规则:取省/市/区中的第一个词
    parts = address.split('省')
    if len(parts) > 1:
        return parts[0] + '省'
    parts = address.split('市')
    if len(parts) > 1:
        return parts[0] + '市'
    return address


'''
.apply() 的核心逻辑就是：“遍历 Series 中的每一个元素，把它们一个一个地扔进你定义的函数里处理，最后把结果收回来。”
.apply() 的返回类型遵循一个核心原则：“看人下菜碟”。它会根据你传入的函数返回值的结构，自动推断最终的结果类型
默认情况：返回 Series
特殊情况：如果你显式要求展开（expand）或返回了 Series 对象，则返回 DataFrame
'''

df_orders_clean['city'] = df_orders_clean['address'].apply(extract_city)
print(df_orders_clean)

# 4. 清洗后数据检查
print("=== 清洗后数据检查 ===")
print("1. 数据质量检查:")
print(f"最终数据形状:{df_orders_clean.shape}")
print("缺失值检查:")
print(df_orders_clean.isna().sum())
print("2. 价格统计:")
print(f"价格均值:{df_orders_clean['price'].mean():.2f}")
print(f"价格中位数:{df_orders_clean['price'].median():.2f}")
print(f"价格标准差:{df_orders_clean['price'].std():.2f}")
# 5. 保存清洗后的数据
print("=== 保存清洗后的数据 ===")
df_orders_clean.to_csv('cleaned_orders.csv', index=False, encoding='utf-8')
print("已保存清洗后的数据到 cleaned_orders.csv")
'''
    原本(11, 8) 'user_id'一行缺失，'order_id'一行重复，sheng'xian, 删除后变成(9, 8)
    提取日期添加一列'order_date',提取地址添加一列'city', 变为(9, 10)
'''
print_star()


# 5.1.2 练习二:员工信息数据清洗
# 数据描述:
# - 数据来源:公司员工信息表
# - 文件格式:Excel（包含多个工作表）
# - 包含字段:员工ID、姓名、性别、年龄、入职日期、部门、职位、薪资、邮箱
# - 数据问题:包含缺失值、重复记录、数据类型错误、邮箱格式不一致
# 清洗要求:
# 1.读取所有工作表数据并合并
# 2.检查并处理重复员工ID
# 3.标准化性别和职位信息
# 4.转换日期格式并计算工龄
# 5.验证邮箱格式并提取域名
# 6.处理薪资异常值

# 练习代码框架:
# 1. 读取Excel数据
# 读取所有工作表
excel_data = pd.read_excel('Data_File/employee_data.xlsx', sheet_name=None)
print("发现的工作表:", list(excel_data.keys()))

"""
当你使用 sheet_name=None 时，Pandas 会读取 Excel 中的所有工作表，并返回一个字典，而不是一个 DataFrame。
字典的键：是工作表的名字（如 'Sheet1', 'Sheet2'）。
字典的值：才是具体的 DataFrame。
所以，当你运行 excel_data['hire_date'] 时，Python 会试图在字典里找一个叫 'hire_date' 的键
（也就是找一个叫 'hire_date' 的 Sheet），当然找不到，所以报了 KeyError。

这样用时可以的
print(excel_data["员工信息_1"]) 
"""

# 合并所有工作表
df_employees = pd.concat(excel_data.values(), ignore_index=True)
# 2. 数据质量检查
print("=== 员工数据质量检查 ===")
print(f"原始数据记录数:{len(df_employees)}")
print(df_employees.info())
# 3. 数据清洗
print("=== 开始数据清洗 ===")
# 处理重复员工ID
print("1. 处理重复员工ID:")
duplicate_ids = df_employees[df_employees.duplicated(subset=['employee_id'], keep=False)]
print(f"发现{len(duplicate_ids)}条重复ID记录")
# 保留最新的记录（假设入职日期越近越准确）

# 生成的数据我还要再洗一遍，洗了，人工清洗果然很麻烦(还洗不完)
# 处理 ISO 标准格式 (2011-03-07)
"""
Pandas 在进行筛选 df[mask] 时，必须明确知道这一行是“要”还是“不要”（True 或 False）
如果你给它一个 NaN，它会困惑：“我不知道这一行该不该选”，于是报错
只需要在 .str.match() 后面加上 na=False 参数即可

下面也是一样
如果 hire_date 这一列里有空值（NaN），.str.contains() 默认会返回 NaN（表示“不知道里面有没有年”），而不是 False
同样只需要在 .str.contains() 里加上 na=False 参数
"""
mask_iso = df_employees['hire_date'].str.match(r'^\d{4}-\d{2}-\d{2}$', na=False)
df_employees.loc[mask_iso, 'hire_date'] = pd.to_datetime(df_employees.loc[mask_iso, 'hire_date'])
# 处理中文格式 (2010年03月07日)
# 技巧：先把 "年" 替换为 "-"，"日" 替换为 ""，变成标准格式再转
mask_cn = df_employees['hire_date'].str.contains('年', na=False)
df_employees.loc[mask_cn, 'hire_date'] = pd.to_datetime(
    df_employees.loc[mask_cn, 'hire_date'].str.replace('年', '-').str.replace('月', '-').str.replace('日', '')
)
# 处理 欧式斜杠格式 (27/05/2018)
# 注意：必须指定 dayfirst=True，否则 27 会被误判
mask_slash = df_employees['hire_date'].str.match(r'^\d{2}/\d{2}/\d{4}$', na=False)
df_employees.loc[mask_slash, 'hire_date'] = pd.to_datetime(
    df_employees.loc[mask_slash, 'hire_date'],
    format='mixed'  # 明确指定：日/月/年
)
"""
Mixed 模式（format='mixed'）
逻辑：Pandas 会逐行扫描。
看到 2021-01-01 -> 识别为 ISO 格式 -> 解析。
看到 27/05/2018 -> 识别为 欧/英 格式 -> 解析。
看到 2010年03月07日 -> 识别为 中文 格式 -> 解析。
后果：无论你的 Excel 表里混了多少种日期写法，它都能自动识别并统一转换成标准时间。

优点：
极其省心：不需要写正则表达式，不需要分步筛选。
兼容性强：完美支持中英文混排、各种分隔符混排。
缺点：
速度稍慢：因为要逐行去“猜”格式，处理几百万行数据时，速度会比指定单一格式（如 format='%Y-%m-%d'）慢一些。但在几十万行数据量下，体感差异不大。
结论：对于现在处理这种清洗任务，format='mixed' 是目前的最优解。
"""

# 强制转换：无法识别的格式（包括那个 int）都会变成 NaT (Not a Time)
df_employees['hire_date'] = pd.to_datetime(
    df_employees['hire_date'],
    errors='coerce',  # 关键参数：遇到无法转换的（如那个 int），直接转为空值，不再报错
    dayfirst=True  # 辅助判断 日/月/年
)

"""
有些日期在 Excel 里虽然显示为 2021/5/20，但底层存储可能是数字 44336。
或者有的单元格是纯数字 20210520，Pandas 读取时把它当成了整数，而不是字符串。
使用 errors='coerce' 可以把这些乱七八糟的格式统统“打回原形”（转为时间或空值），是清洗数据的终极手段。
"""

df_employees_clean = df_employees.sort_values('hire_date', ascending=False)
df_employees_clean = df_employees_clean.drop_duplicates(subset=['employee_id'], keep='first')
print(f"处理后剩余记录数:{len(df_employees_clean)}")
# 标准化性别（转换为'男'或'女'）
print("2. 标准化性别:")
gender_mapping = {
    '男': '男', '男性': '男', 'M': '男', 'm': '男',
    '女': '女', '女性': '女', 'F': '女', 'f': '女',
    '未知': None, '未填写': None
}
df_employees_clean['gender'] = df_employees_clean['gender'].map(gender_mapping)
# 标准化职位（简化处理）
print("3. 标准化职位:")
position_mapping = {
    '工程师': '工程师', '开发工程师': '工程师', '软件工程师': '工程师',
    '产品经理': '产品经理', '产品': '产品经理',
    '销售': '销售', '客户经理': '销售',
    '运营': '运营', '数据运营': '运营'
}


def standardize_position(pos):
    """标准化职位名称"""
    if pd.isna(pos):
        return None
    for key in position_mapping:
        if key in pos:
            return position_mapping[key]
    return '其他'


df_employees_clean['position'] = df_employees_clean['position'].apply(standardize_position)
# 日期处理和工龄计算
print("4. 日期处理和工龄计算:")
# 转换入职日期
df_employees_clean['hire_date'] = pd.to_datetime(df_employees_clean['hire_date'], errors='coerce')
# 计算工龄（年）
current_date = datetime.datetime(2026, 4, 28)  # 假设当前日期
df_employees_clean['work_years'] = (current_date - df_employees_clean['hire_date']).dt.days / 365
# 验证邮箱格式
print("5. 验证邮箱格式:")


def validate_email(email):
    """验证邮箱格式并提取域名"""
    if pd.isna(email):
        return None, None
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$'
    if re.match(pattern, email):
        domain = email.split('@')[1]
        return email, domain
    return None, None


# 提取邮箱和域名
emails, domains = zip(*df_employees_clean['email'].apply(validate_email))
df_employees_clean['valid_email'] = list(emails)
df_employees_clean['email_domain'] = list(domains)
# 处理薪资异常值

# 1. 强制转换 salary 列为数字
# errors='coerce' 的意思是：如果遇到 "面议" 或 "10k" 这种转不成数字的，直接变成空值 (NaN)
df_employees_clean['salary'] = pd.to_numeric(df_employees_clean['salary'], errors='coerce')

print("6. 处理薪资异常值:")
print("薪资统计:")
print(f"薪资范围:{df_employees_clean['salary'].min():.0f} - {df_employees_clean['salary'].max():.0f}")
print(f"薪资均值:{df_employees_clean['salary'].mean():.0f}")
print(f"薪资中位数:{df_employees_clean['salary'].median():.0f}")
# 使用IQR方法检测异常值
q1 = df_employees_clean['salary'].quantile(0.25)
q3 = df_employees_clean['salary'].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
outliers = df_employees_clean[(df_employees_clean['salary'] < lower_bound) |
                              (df_employees_clean['salary'] > upper_bound)]
print(f"检测到{len(outliers)}个薪资异常值")
# 将异常值设为中位数（保守处理）
df_employees_clean['salary'] = df_employees_clean['salary'].where(
    (df_employees_clean['salary'] >= lower_bound) & (df_employees_clean['salary'] <= upper_bound),
    df_employees_clean['salary'].median()
)
# 4. 数据质量复查
print("=== 清洗后数据质量复查 ===")
print(f"最终数据记录数:{len(df_employees_clean)}")
print("主要指标统计:")
print(f"平均年龄:{df_employees_clean['age'].mean():.1f}岁")
print(f"平均工龄:{df_employees_clean['work_years'].mean():.1f}年")
print(f"员工分布（按部门）:")
print(df_employees_clean['department'].value_counts())
print(f"员工分布（按职位）:")
print(df_employees_clean['position'].value_counts())
# 5. 保存结果
df_employees_clean.to_excel('cleaned_employees.xlsx', index=False, sheet_name='清洗后员工数据')
print("已保存清洗后的数据到 cleaned_employees.xlsx")
print_star()
"""
验证邮箱的代码看起来是对的，实际也算是对的，因为我生成数据的时候没有表述清楚，所以大部分是没有数据的
"""


# 5.2 多表合并清洗练习
# 5.2.1 练习三:销售数据整合
"""
数据描述:
- 数据来源:三个 CSV 文件（销售订单、产品信息、客户信息）
    - 文件1:sales_orders.csv - 销售订单（订单ID、客户ID、产品ID、数量、日期）
    - 文件2:products.csv - 产品信息（产品ID、产品名称、类别、单价）
    - 文件3:customers.csv - 客户信息（客户ID、客户名称、城市、国家）
- 数据问题:订单中存在无效的产品ID和客户ID、数量异常、日期格式不一致
清洗要求:
    1.读取并清洗三个数据表
    2.验证订单中的外键（产品ID和客户ID）
    3.计算订单金额
    4.按产品类别和客户国家进行销售统计
    5.找出异常订单（数量为负或超过100）
"""
# 练习代码框架:
# 1. 读取并清洗三个数据表
print("=== 销售数据整合与清洗 ===")
# 读取订单数据
print("1. 读取并清洗订单数据:")
'''
    pandas加载csv文件的常用格式
    pd.read_csv('...csv', encoding='utf-8')
    encoding= 就是指定 CSV 文件的编码格式！
    
    encoding='utf-8-sig'
    它 = 带「签名」的 UTF-8 编码
    作用：专门解决 Excel 保存的 CSV 中文乱码问题
    它是 pandas 读取中文 CSV 最稳、最推荐的编码！
    
    编码	        说明	                适用场景
    utf-8	    普通 UTF-8，不带签名	代码生成的文件、Linux/Mac 生成的文件
    utf-8-sig	带签名的 UTF-8	    Excel 保存的 CSV、Windows 导出的中文文件
    
    Excel 保存 CSV 时，会偷偷在文件开头加一个「看不见的标记」—— 叫 BOM
    如果你用 utf-8 读取：
    会把这个标记当成乱码
    结果就是：第一列表头出现 ï»¿ 奇怪符号
    用 utf-8-sig：
    会自动识别并忽略这个 BOM 标记
    中文完美显示，不乱码 ✅
    
    sig = BOM Signature(BOM 签名)
'''
df_orders = pd.read_csv('Data_File/sales_orders.csv', encoding='utf-8-sig')
print(f"订单数据形状:{df_orders.shape}")
# 清洗订单数据
# 转换日期格式
df_orders['order_date'] = pd.to_datetime(df_orders['order_date'], errors='coerce')
'''
    df_orders['order_date'] = pd.to_datetime(df_orders['order_date'], errors='coerce')
    把混乱的日期文本，统一变成标准日期格式
    遇到无法识别的错误日期，直接转成空值（NaT）
    
    1. pd.to_datetime(...)
    功能：把字符串 / 数字 → 转换成 pandas 能识别的 日期时间类型
    比如：
        "2025-01-01" → 标准日期
        "01/02/2025" → 标准日期
        "2025.01.03" → 标准日期
    2. errors='coerce' （最关键）
    意思：遇到无法识别的错误日期，不强转，不报错，而是转成空值 NaT
    例子：
        "今天" → NaT
        "abc123" → NaT
        "2025/13/32" → NaT
    作用：让你的代码不会因为脏日期崩溃！
    3. 赋值给 df_orders['order_date']
    把原来混乱的日期列，覆盖成干净、标准、可计算的日期格式
'''

# 处理异常数量（数量不能为负，且不超过100）, 和前面的例子类似
df_orders['quantity'] = df_orders['quantity'].where(
    (df_orders['quantity'] > 0) & (df_orders['quantity'] <= 100),
    1  # 将异常数量设为1
)
# 读取产品数据
print("2. 读取并清洗产品数据:")
df_products = pd.read_csv('Data_File/products.csv', encoding='utf-8')
print(f"产品数据形状:{df_products.shape}")
# 清洗产品数据（去除重复产品ID）
df_products_clean = df_products.drop_duplicates(subset=['product_id'])
'''
    drop_duplicates()
    Pandas 去重方法，默认：
        整行所有字段完全相同，才判定为重复；
    subset=['product_id']
        限定去重依据：
        只看 product_id 这一列只要 product_id 重复 → 判定为重复行，直接删除
    保留规则
        默认参数：keep='first'
        重复的产品 ID → 保留第一行，删除后面所有重复行
'''

# 读取客户数据
print("3. 读取并清洗客户数据:")
df_customers = pd.read_csv('Data_File/customers.csv', encoding='utf-8')
print(f"客户数据形状:{df_customers.shape}")
# 清洗客户数据（去除重复客户ID）
df_customers_clean = df_customers.drop_duplicates(subset=['customer_id'])

# 2. 数据验证和合并
print("=== 数据验证与合并 ===")
# 验证订单中的产品ID
valid_product_ids = set(df_products_clean['product_id'])
invalid_orders = df_orders[~df_orders['product_id'].isin(valid_product_ids)]
'''
    valid_product_ids = 合法产品 ID 清单
    invalid_orders = 订单里的无效数据（用了不存在的产品）
    ~ = 不是、取反
    .isin() = 是否在列表里
    
    Series 是可迭代对象
    set() 可以接收任何可迭代对象（列表、Series、数组…）
    
    ✅ 布尔 Series 完全可以像 bool 列表一样筛选 DataFrame！
'''

print(f"发现{len(invalid_orders)}条包含无效产品ID的订单")

# 验证订单中的客户ID
valid_customer_ids = set(df_customers_clean['customer_id'])
invalid_orders = df_orders[~df_orders['customer_id'].isin(valid_customer_ids)]
print(f"发现{len(invalid_orders)}条包含无效客户ID的订单")

# 合并数据
print("4. 合并订单、产品和客户数据:")
# 先合并订单和产品
df_orders_products = pd.merge(
    df_orders,                # 左表：订单
    df_products_clean[['product_id', 'product_name', 'category', 'unit_price']],  # 右表：产品（只取需要的列）
    on='product_id',          # 按产品ID合并（共同列）
    how='inner'               # 内连接：只保留两边都有的数据
)
# 再合并客户信息
df_full_data = pd.merge(
    df_orders_products,     # 左表：订单+产品
    df_customers_clean[['customer_id', 'customer_name', 'city', 'country']],  # 右表：客户
    on='customer_id',      # 按客户ID合并
    how='inner'            # 内连接：只保留有效客户
)
'''
    上面是多表关联数据分析最核心、最标准的写法！
    
    pd.merge() = 多表拼接（SQL 里的 join）
    on='字段' = 按哪个共同字段拼接
    how='inner' = 只保留两边都能匹配上的数据（有效数据）
    代码 = 订单 + 产品 + 客户 → 拼接成一张完整干净的大表
'''
print(f"合并后的数据形状:{df_full_data.shape}")

# 3. 计算订单金额
print("5. 计算订单金额:")
# 原来应该没有这一列, 应该是向量化计算, 添加新列
df_full_data['order_amount'] = df_full_data['quantity'] * df_full_data['unit_price']

# 4. 销售统计
print("6. 销售统计分析:")
# 按产品类别统计销售
category_sales = df_full_data.groupby('category').agg({
    'order_amount': 'sum',
    'quantity': 'sum',
    'order_id': 'count'
}).rename(columns={'order_id': 'order_count'})
'''
    1. groupby('category')
        按「产品类别」分组, 每组单独统计
    2. .agg({ ... }) 聚合统计
        agg = aggregate 聚合可以一次性对不同列做不同计算
        'order_amount': 'sum'    → 金额【求和】
        'quantity': 'sum'        → 数量【求和】
        'order_id': 'count'      → 订单【计数】（算有多少笔订单）
    3. .rename(columns={'order_id': 'order_count'})
        把默认列名 order_id → 改成 order_count（订单数）
        让结果表更清晰、更专业
        
    返回值类型是 → DataFrame
    行索引(index) ← 由 groupby(字段) 指定
    列名(columns) ← 由 agg({字典}) 指定
'''
print("按产品类别销售统计:")
print(category_sales)

# 按国家统计销售
country_sales = df_full_data.groupby('country').agg({
    'order_amount': 'sum',
    'customer_id': 'nunique'
}).rename(columns={'customer_id': 'customer_count'})
'''
    nunique = Number of unique→ 不重复的个数 / 去重后的数量
'''
print("按国家销售统计:")
print(country_sales)

# 5. 找出异常订单
print("7. 异常订单检测:")
# 找出金额超过10000的订单
high_value_orders = df_full_data[df_full_data['order_amount'] > 10000]
print(f"高价值订单（>10000）:{len(high_value_orders)}条")
# 找出单价异常的订单（单价超过1000）
high_price_orders = df_full_data[df_full_data['unit_price'] > 1000]
print(f"高单价订单（单价>1000）:{len(high_price_orders)}条")

# 6. 保存结果
print("=== 保存整合后的数据 ===")
df_full_data.to_csv('integrated_sales_data.csv', index=False, encoding='utf-8')
print("已保存整合后的数据到 integrated_sales_data.csv")

# 保存统计报表
# 数据验证
print("category_sales 形状：", category_sales.shape)
print("country_sales 形状：", country_sales.shape)
print("df_full_data 形状：", df_full_data.shape)

with pd.ExcelWriter('sales_report2.xlsx') as writer:
    '''
        pd.ExcelWriter：pandas 的 Excel 写入器
        with ... as writer: 自动打开 / 关闭文件，安全不报错
    '''
    df_full_data.to_excel(writer, sheet_name='完整销售数据', index=False)
    '''
        把完整清洗后的大表写入
        sheet_name：工作表名字
        index=False：不导出 pandas 行号（干净整洁）
    '''
    category_sales.to_excel(writer, sheet_name='按类别统计', index=True)
    country_sales.to_excel(writer, sheet_name='按国家统计', index=True)
    '''
        把分组统计结果写入
        index=True：导出行索引（类别 / 国家）
        因为 groupby 后，索引是类别 / 国家，必须导出才完整！
    '''
print("已生成销售统计报表 sales_report2.xlsx")
print_star()


# 5.2
# .2
# 练习四:多源数据合并
# 数据描述:
# - 数据来源:
# - 主数据表:main_data.csv - 包含
# ID、姓名、年龄、性别
# - 补充数据表
# 1:supplement1.csv - 包含
# ID、收入、职业
# - 补充数据表
# 2:supplement2.csv - 包含
# ID、教育背景、联系方式
# - 数据问题:ID
# 格式不一致、有缺失数据、重复记录
# 清洗要求:
# 1.
# 读取所有数据并统一
# ID
# 格式
# 2.
# 合并三个数据集
# 3.
# 处理冲突数据（如不同来源的收入数据）
# 4.
# 填充缺失值
# 5.
# 进行基本统计分析
# 练习代码框架:
# # 1. 读取并清洗数据
# import pandas as pd
# import numpy as np
# print("=== 多源数据合并清洗 ===")
# # 读取主数据
# print("1. 读取主数据:")
# df_main = pd.read_csv('main_data.csv', encoding='utf-8')
# print(f"主数据形状:{df_main.shape}")
# print("主数据示例:")
# print(df_main.head())
# # 读取补充数据1
# print("2. 读取补充数据1:")
# df_supp1 = pd.read_csv('supplement1.csv', encoding='utf-8')
# print(f"补充数据1形状:{df_supp1.shape}")
# # 读取补充数据2
# print("3. 读取补充数据2:")
# df_supp2 = pd.read_csv('supplement2.csv', encoding='utf-8')
# print(f"补充数据2形状:{df_supp2.shape}")
# # 2. 统一ID格式
# print("=== 统一ID格式 ===")
# # 观察ID格式
# print("主数据ID格式示例:", df_main['ID'].iloc[0])
# print("补充数据1 ID格式示例:", df_supp1['id'].iloc[0])
# print("补充数据2 ID格式示例:", df_supp2['user_id'].iloc[0])
# # 假设需要将所有ID转换为统一格式（如去掉前缀）
# def clean_id(id_str):
#     """清洗ID格式"""
#     if pd.isna(id_str):
#         return None
#     # 去掉非数字字符
#     cleaned = ''.join([c for c in str(id_str) if c.isdigit()])
#     return cleaned
# # 清洗所有ID列
# df_main['clean_id'] = df_main['ID'].apply(clean_id)
# df_supp1['clean_id'] = df_supp1['id'].apply(clean_id)
# df_supp2['clean_id'] = df_supp2['user_id'].apply(clean_id)
# # 3. 数据合并
# print("=== 数据合并 ===")
# # 先合并主数据和补充数据1
# df_merged1 = pd.merge(
#     df_main,
#     df_supp1[['clean_id', 'income', 'occupation']],
#     on='clean_id',
#     how='outer',
#     suffixes=('', '_supp1')
# )
# # 再合并补充数据2
# df_merged = pd.merge(
#     df_merged1,
#     df_supp2[['clean_id', 'education', 'contact']],
#     on='clean_id',
#     how='outer',
#     suffixes=('', '_supp2')
# )
# print(f"合并后数据形状:{df_merged.shape}")
# # 4. 处理冲突数据
# print("=== 处理数据冲突 ===")
# # 检查是否有冲突的数据（如不同来源的收入数据）
# print("检查收入数据冲突:")
# conflict_income = df_merged[
#     (~df_merged['income'].isna()) &
#     (~df_merged['income_supp1'].isna()) &
#     (df_merged['income'] != df_merged['income_supp1'])
#     ]
# print(f"发现{len(conflict_income)}条收入数据冲突")
# # 处理冲突:优先使用补充数据1的收入（假设更可靠）
# df_merged['final_income'] = df_merged['income_supp1'].fillna(df_merged['income'])
# # 类似处理其他冲突数据
# print("检查职业数据冲突:")
# conflict_occupation = df_merged[
#     (~df_merged['occupation'].isna()) &
#     (~df_merged['occupation_supp1'].isna()) &
#     (df_merged['occupation'] != df_merged['occupation_supp1'])
#     ]
# print(f"发现{len(conflict_occupation)}条职业数据冲突")
# # 5. 填充缺失值
# print("=== 填充缺失值 ===")
# # 统计缺失值
# missing_summary = df_merged.isna().sum()
# print("缺失值统计:")
# print(missing_summary)
# # 填充策略:
# # - 数值型:用均值或中位数
# # - 字符串型:用最频繁的值或'未知'
# # - 日期型:可能需要特殊处理
# # 填充年龄（用均值）
# df_merged['age'] = df_merged['age'].fillna(df_merged['age'].mean())
# # 填充性别（用众数）
# df_merged['gender'] = df_merged['gender'].fillna(df_merged['gender'].mode()[0])
# # 填充教育背景（用'未知'）
# df_merged['education'] = df_merged['education'].fillna('未知')
# # 填充联系方式（用'未提供'）
# df_merged['contact'] = df_merged['contact'].fillna('未提供')
# # 6. 数据质量检查
# print("=== 清洗后数据质量检查 ===")
# print("最终数据形状:", df_merged.shape)
# print("缺失值检查:")
# print(df_merged.isna().sum())
# # 7. 基本统计分析
# print("=== 基本统计分析 ===")
# # 按性别统计
# gender_stats = df_merged.groupby('gender').agg({
#     'age': 'mean',
#     'final_income': 'mean',
#     'occupation': 'nunique'
# }).round(1)
# print("按性别统计:")
# print(gender_stats)
# # 按职业统计
# occupation_stats = df_merged.groupby('occupation').agg({
#     'final_income': 'mean',
#     'age': 'mean',
#     'education': 'nunique'
# }).round(1)
# print("按职业统计:")
# print(occupation_stats.head(10))
# # 收入分布分析
# print("收入分布分析:")
# income_bins = [0, 5000, 10000, 20000, 30000, float('inf')]
# income_labels = ['0-5K', '5-10K', '10-20K', '20-30K', '30K+']
# df_merged['income_level'] = pd.cut(df_merged['final_income'], bins=income_bins, labels=income_labels)
# income_dist = df_merged['income_level'].value_counts().sort_index()
# print(income_dist)
# # 8. 保存结果
# print("=== 保存最终数据 ===")
# # 选择需要保留的列
# final_columns = [
#     'clean_id', 'name', 'age', 'gender',
#     'final_income', 'occupation', 'education', 'contact'
# ]
# df_final = df_merged[final_columns]
# df_final.to_csv('cleaned_merged_data.csv', index=False, encoding='utf-8')
# print("已保存清洗合并后的数据到 cleaned_merged_data.csv")
# # 生成数据报告
# with pd.ExcelWriter('data_analysis_report.xlsx') as writer:
#     df_final.to_excel(writer, sheet_name='清洗后完整数据', index=False)
#     gender_stats.to_excel(writer, sheet_name='性别统计', index=True)
#     occupation_stats.to_excel(writer, sheet_name='职业统计', index=True)
#     income_dist.to_frame().to_excel(writer, sheet_name='收入分布', index=True)
# print("已生成数据分析报告 data_analysis_report.xlsx")


"""
六、总结与扩展
6.1 数据清洗流程总结
经过本教程的学习，你已经掌握了使用 Pandas 进行数据清洗的核心技能一个完整的数据清洗流程通常包括以下步骤:
1.数据读取与初步检查（5-10分钟）
- 读取数据文件
- 检查数据形状、基本信息
- 初步了解数据结构和内容

2.数据质量全面评估（15-20分钟）
- 缺失值检测与统计
- 重复值检测
- 异常值检测
- 数据类型检查
- 逻辑一致性检查

3.制定清洗策略（5-10分钟）
- 根据数据质量评估结果制定计划
- 确定处理优先级（如必须保留的关键列）
- 选择合适的清洗方法

4.执行数据清洗（30-60分钟）
- 处理缺失值（删除或填充）
- 处理重复值
- 数据类型转换
- 字符串清洗
- 日期标准化
- 异常值处理

5.高级清洗技术应用（20-30分钟）
- 分组清洗
- 条件清洗
- 数据标准化 / 归一化
- 文本数据特殊处理

6.清洗结果验证（10-15分钟）
- 再次检查数据质量
- 验证关键指标
- 确保数据完整性

7.数据保存与报告（5-10分钟）
- 保存清洗后的数据
- 生成清洗报告
- 记录清洗过程和决策
"""

"""
6.2
常见问题与解决方案
在数据清洗过程中，经常遇到以下问题:
1.中文编码问题
- 问题:读取中文CSV文件时出现乱码
    - 解决方案:使用encoding = 'gbk'或encoding = 'utf-8-sig'参数

2.混合类型列
- 问题:同一列中包含多种数据类型
    - 解决方案:
    - 使用dtype参数显式指定类型
    - 使用to_numeric配合errors = 'coerce'
    - 分离为多个列

3.大文件处理
- 问题:文件过大无法一次性加载到内存
    - 解决方案:
    - 使用chunksize参数分块读取
    - 使用usecols只读取需要的列
    - 逐步处理数据

4.日期格式不统一
- 问题:日期格式多样（如"2025/04/01"、"2025-04-01"、"01-04-2025"）
    - 解决方案:
    - 使用to_datetime配合format参数
    - 先统一为字符串格式，再转换
    - 处理不同地区的日期格式

5.数据冲突
- 问题:多个数据源提供了不同的值
    - 解决方案:
    - 确定数据优先级
    - 记录冲突并人工审核
    - 使用统计方法（如取均值）

6.性能问题
- 问题:处理大数据集时速度慢
    - 解决方案:
    - 使用向量化操作代替循环
    - 选择合适的数据类型（如使用category类型）
    - 使用更高效的算法
"""

"""
6.3进阶学习建议
为了进一步提升数据清洗技能，建议:
1.学习更多Pandas高级功能
    - 深入了解groupby和apply的高级用法
    - 学习使用pivot_table进行数据透视
    - 掌握时间序列数据处理方法

2.扩展数据格式处理能力
    - 学习处理JSONLines格式
    - 掌握处理嵌套JSON的方法
    - 学习处理Parquet、ORC等列式存储格式
    - 了解如何处理数据库数据

3.提升文本处理技能
    - 深入学习正则表达式
    - 了解自然语言处理（NLP）技术
    - 学习使用spaCy、NLTK等库

4.掌握更多清洗技术
    - 学习处理地理空间数据
    - 了解数据验证规则引擎
    - 学习使用dask进行并行处理

5.实践真实项目
    - 参与Kaggle数据竞赛
    - 尝试清洗真实业务数据
    - 学习数据质量评估标准

6.了解数据治理
    - 学习数据质量管理体系
    - 了解数据合规要求
    - 学习数据版本控制

记住，数据清洗是一个不断迭代的过程，需要根据具体数据和业务需求灵活调整策略。不断实践和总结经验。
"""

"""
6.4
练习答案与提示
为帮助你完成练习，以下提供部分练习的答案要点:

练习一答案要点:
1.缺失值处理后剩余记录数:995
条（假设原始有1000条，5条因关键列缺失被删除）
2.重复订单处理:删除5条重复订单
3.异常价格处理:将负价格和超高价格设为中位数
4.日期格式转换:成功转换为datetime格式
5.城市提取:从地址中提取出城市名

练习二答案要点:
1.合并后数据:约500条记录（假设三个工作表分别有200、180、120条）
2.重复ID处理:删除约20条重复记录
3.性别标准化:统一为' 男'或' 女'，约5条' 未知'
4.工龄计算:平均工龄约5.3年
5.邮箱验证:约95 % 的邮箱格式正确

练习三答案要点:
1.订单验证:约20条无效产品ID，15条无效客户ID
2.合并后数据:约965条有效订单
3.按类别销售:电子产品占比最高（约40 %）
4.按国家销售:中国占比最高（约60 %）
5.异常订单:10条高价值订单（ > 10000）

练习四答案要点:
1.ID统一:成功将不同格式的ID转换为统一格式
2.数据合并:合并后约380条记录（原始三个数据集分别有150、140、130条）
3.冲突处理:处理了约15条收入冲突，20条职业冲突
4.缺失值填充:年龄用均值（32.5岁），性别用众数（' 男 '）
5.统计分析:男性平均收入略高于女性，技术类职业收入最高
记住，实际答案可能因数据不同而有所差异。重点是掌握数据清洗的方法和思路，而不是具体的数值结果
"""
