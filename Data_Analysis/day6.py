import pandas as pd
import openpyxl


# 数据输入输出
def print_dot():
    print(50 * ".")


def print_star():
    print(50 * "*")


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
    usecols=None,  # 指定读取哪些列
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
    # 表头（列名）：Name, Age, City → 不算行
    # 第一行数据：索引 0 → 算行，会被 head () 包含
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
# df_parquet = pd.read_parquet('data.parquet')
# print("读取Parquet文件:")
# print(df_parquet.head())
# 写入Parquet文件
# df_to_parquet = pd.DataFrame({
#     'Name': ['Alice', 'Bob', 'Charlie', 'David'],
#     'Score': [85.5, 90.0, 78.5, 88.0]
# })
# df_to_parquet.to_parquet('output.parquet')
# print("写入Parquet文件:")
# print("文件已保存到output.parquet")

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
