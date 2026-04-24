import pandas as pd
import numpy as np


# Pandas 基础概念与环境配置
# 1.1 Pandas 简介与核心优势
# Pandas 是 Python 的核心数据分析库，专为处理结构化数据（如表格、时间序列）设计
# 它提供了两个核心数据结构: Series（一维带标签数组）和DataFrame（二维表格型数据结构）
# Pandas 的主要优势包括:
# 标签化索引: 支持基于标签的灵活数据选择，而非仅依赖位置索引
# 异构数据类型: DataFrame 的不同列可以存储不同类型的数据
# 高效的数据对齐: 自动按索引对齐不同数据源的数据
# 丰富的数据处理功能: 从数据清洗到复杂分析的完整工具链
# 时间序列支持: 强大的时间数据处理和频率转换功能

# Pandas 与 NumPy 的关系
# 核心关系:
# Pandas 是建立在 NumPy 之上的库，其核心数据结构底层是基于 NumPy 数组构建的
# NumPy 是 “数字计算器”，Pandas 是 “表格管理器”
# NumPy 更适合处理纯数值型数据，Pandas 更适合处理带标签的表格数据

# 关键区别:
# 特性	     NumPy	             Pandas
# 数据结构	 ndarray（多维数组）	 Series、DataFrame
# 索引方式	 仅支持整数索引	     支持标签索引和位置索引
# 数据类型	 同构类型	             异构类型（DataFrame）
# 缺失值处理	 有限支持(强制转为浮点)  原生支持 NaN
# 适用场景	 数值计算、矩阵运算	     表格数据、时间序列分析


# 2.1 Series 的创建
# Series 是 Pandas 的核心一维数据结构，可以理解为 “带索引的列表”
# 从 Python 列表创建
# 最基本的创建方式是从列表创建 Series
# 创建一个简单的Series，使用默认索引
s1 = pd.Series([10, 20, 30, 40])
print("s1:")
# 输出时会自动输出 dtype 类型
print(s1)
print(f"数据类型: {s1.dtype}")
print(f"索引类型: {type(s1.index)}")
# 输出结果:
# 0    10
# 1    20
# 2    30
# 3    40
# dtype: int64
print(50 * ".")

# 指定自定义索引
# 创建时可以指定自定义索引
# 创建时指定自定义索引
custom_index = ['a', 'b', 'c', 'd']
s2 = pd.Series([10, 20, 30, 40], index=custom_index)
print("s2:")
print(s2)
# 输出结果:
# a    10
# b    20
# c    30
# d    40
# dtype: int64
print(50 * ".")

# 从字典创建
# 从字典创建 Series 时，字典的键会自动成为索引:
# 从字典创建，字典键自动成为索引
data_dict = {'a': 10, 'b': 20, 'c': 30, 'd': 40}
s3 = pd.Series(data_dict)
print("s3:")
print(s3)
# 输出结果:
# a    10
# b    20
# c    30
# d    40
# dtype: int64
print(50 * ".")

# 从 NumPy 数组创建
np_array = np.array([10, 20, 30, 40])
s4 = pd.Series(np_array, index=['w', 'x', 'y', 'z'])
print("s4:")
print(s4)
# 输出结果:
# w    10
# x    20
# y    30
# z    40
# dtype: int32
print(50 * ".")

# 创建特定值的 Series
# 你还可以创建包含特定值的 Series
# 创建全为5的Series，长度为5
s5 = pd.Series(5, index=['a', 'b', 'c', 'd', 'e'])
print("s5:")
print(s5)
# 输出结果:
# a    5
# b    5
# c    5
# d    5
# e    5
# dtype: int64

# | 变量  | 输入来源             | pandas 的行为              | 结果 dtype      |
# | `s4` | `np.array([...])`  | **继承** numpy 数组的 dtype | 取决于 numpy 默认值 |
# | `s5` | Python 标量 `5`     | **自己推断**最合适的 dtype   | 通常是 `int64`   |
# s4 的 dtype 由 numpy 决定（平台相关），s5 的 dtype 由 pandas 决定（统一用 int64）
# 两者调用的是同一个 pd.Series，但内部走的数据处理路径不同

print(50 * "*")


# 2.2 Series 的基本属性
# Series 具有以下核心属性
# index: 获取索引
# values: 获取数据值（返回 NumPy 数组）

print("s2的索引:", s2.index)
print("s2的值:", s2.values)
print(f"值的类型: {type(s2.values)}")
# 输出结果:
# s2的索引: Index(['a', 'b', 'c', 'd'], dtype='object')
# s2的值: [10 20 30 40]
# 值的类型: <class 'numpy.ndarray'>
print(50 * ".")

# 数据类型
# dtype: 获取数据类型
# astype(): 转换数据类型
print(f"s2的数据类型: {s2.dtype}")
# 转换为浮点类型
s2_float = s2.astype(float)
print(f"s2_float的数据类型: {s2_float.dtype}")
# 转换为字符串类型
s2_str = s2.astype(str)
print(f"s2_str的数据类型: {s2_str.dtype}")
print(f"s2_str的值: {s2_str.values}")
# 输出结果:
# s2的数据类型: int64
# s2_float的数据类型: float64
# s2_str的数据类型: object
# s2_str的值: ['10' '20' '30' '40']
print(50 * ".")

# 名称属性
# Series 可以有名称属性，这在数据处理中很有用
# 创建带有名称的Series
s6 = pd.Series([10, 20, 30, 40], index=['a', 'b', 'c', 'd'], name='scores')
print("s6:")
print(s6)
print(f"名称: {s6.name}")
# 输出结果:
# a    10
# b    20
# c    30
# d    40
# Name: scores, dtype: int64
print(50 * ".")


# 2.3 Series 的索引与选择
# Series 支持多种索引方式，这是 Pandas 的强大特性之一
# 基于标签的索引（推荐）
# 使用 **[]或.loc[]** 进行标签索引
print("s2['b']:", s2['b'])  # 直接使用标签
print("s2.loc['c']:", s2.loc['c'])  # 使用loc方法
print("s2.loc[['b', 'd']]:")
print(s2.loc[['b', 'd']])  # 使用列表选择多个标签
print("s2[['b', 'd']:")
print(s2[['b', 'd']])
# 输出结果:
# s2['b']: 20
# s2.loc['c']: 30
# s2.loc[['b', 'd']]:
# b    20
# d    40
# dtype: int64
# s2[['b', 'd']:
# b    20
# d    40
# dtype: int64

# 传单个标签和传列表是完全不同的机制
# 写法	          结果	               说明
# s2['b']	      20	               取单个值，返回标量
# s2[['b', 'd']]  ✅ 返回一个子 Series   传列表，取多个标签
# s2['b', 'd']	  ❌ KeyError	       传的是元组，pandas 把它当成一个整体标签去找
# 取单个标签用 s2['x']，取多个标签必须用 s2[['x', 'y']]（里面套个列表）
# 不能写成 s2['x', 'y']（元组会被当成一个整体标签
print(50 * ".")

# 基于位置的索引
# 使用 **.iloc[]** 进行位置索引（类似 NumPy）
print("s2.iloc[0]:", s2.iloc[0])  # 第一个元素
print("s2.iloc[2]:", s2.iloc[2])  # 第三个元素
print("s2.iloc[1:3]:")
print(s2.iloc[1:3])  # 切片，不包含结束位置
# 输出结果:
# s2.iloc[0]: 10
# s2.iloc[2]: 30
# s2.iloc[1:3]:
# b    20
# c    30
# dtype: int64
print(50 * ".")

# 混合索引注意事项
# 当索引是整数时要特别注意
# 创建整数索引的Series
s_int = pd.Series([10, 20, 30, 40], index=[1, 2, 3, 4])
print("s_int:")
print(s_int)
# 标签索引 → 找标签为 2 的元素
# s_int[2] → pandas 看到整数 2，优先当作标签 → 返回标签 2 对应的 20
print("s_int[2]:", s_int[2])  # 标签索引
# s_int.iloc[2] → 明确按位置 → 返回索引位置 2（第3个）对应的 30
# 位置索引 → 找第 3 个位置（从0开始）的元素
print("s_int.iloc[2]:", s_int.iloc[2])  # 位置索引
# 输出结果:
# s_int:
# 1    10
# 2    20
# 3    30
# 4    40
# dtype: int64
# s_int[2]: 20
# s_int.iloc[2]: 30

# 当索引是整数时，[] 的行为不可预测，始终使用显式方法
# 目的	    推荐写法	        不推荐
# 按标签取值	s_int.loc[2]	s_int[2]
# 按位置取值	s_int.iloc[2]	—
# 索引是整数时，[] 优先当标签用；要按位置取必须用 .iloc，要保险就永远用 .loc / .iloc
print(50 * "*")

# 2.4 Series 的运算操作
# Series 支持多种运算操作，充分利用了向量化特性
# 算术运算
s_a = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
s_b = pd.Series([10, 20, 30, 40], index=['a', 'b', 'c', 'd'])
print("s_a + s_b:")
print(s_a + s_b)
print("s_a * 2:")
print(s_a * 2)
print("s_a / s_b:")
print(s_a / s_b)
# 输出结果:
# s_a + s_b:
# a    11
# b    22
# c    33
# d    44
# dtype: int64
# s_a * 2:
# a     2
# b     4
# c     6
# d     8
# dtype: int64
# s_a / s_b:
# a    0.1
# b    0.1
# c    0.1
# d    0.1
# dtype: float64
print(50 * ".")

# 逻辑运算
print("s_a > 2:")
print(s_a > 2)
print("s_a[s_a > 2]:")
print(s_a[s_a > 2])  # 布尔索引
# 输出结果:
# s_a > 2:
# a    False
# b    False
# c     True
# d     True
# dtype: bool
# s_a[s_a > 2]:
# c    3
# d    4
# dtype: int64
print(50 * ".")

# 与标量运算
print("s_a + 100:")
print(s_a + 100)
print("s_a * 10:")
print(s_a * 10)
# 输出结果:
# s_a + 100:
# a    101
# b    102
# c    103
# d    104
# dtype: int64
# s_a * 10:
# a    10
# b    20
# c    30
# d    40
# dtype: int64
print(50 * "*")


# 2.5 Series 的基本方法
# Series 提供了丰富的统计方法
s_stats = pd.Series([10, 20, 30, 40, 50])
print(f"求和: {s_stats.sum()}")
print(f"均值: {s_stats.mean():.2f}")
print(f"中位数: {s_stats.median():.2f}")
print(f"标准差: {s_stats.std():.2f}")
print(f"最大值: {s_stats.max()}")
print(f"最小值: {s_stats.min()}")
print(f"数据个数: {s_stats.count()}")
# 输出结果:
# 求和: 150
# 均值: 30.00
# 中位数: 30.00
# 标准差: 15.81
# 最大值: 50
# 最小值: 10
# 数据个数: 5
print(50 * ".")

# 排序方法
s_sort = pd.Series([30, 10, 40, 20])
print("原始s_sort:")
print(s_sort)
print("按值升序排序:")
print(s_sort.sort_values())
print("按值降序排序:")
print(s_sort.sort_values(ascending=False))
print("按索引排序:")
print(s_sort.sort_index())
# 输出结果:
# 原始s_sort:
# 0    30
# 1    10
# 2    40
# 3    20
# dtype: int64
# 按值升序排序:
# 1    10
# 3    20
# 0    30
# 2    40
# dtype: int64
# 按值降序排序:
# 2    40
# 0    30
# 3    20
# 1    10
# dtype: int64
# 按索引排序:
# 0    30
# 1    10
# 2    40
# 3    20
# dtype: int64
print(50 * ".")

# 其他常用方法
# unique() - 获取唯一值
s_unique = pd.Series([1, 2, 2, 3, 3, 3])
print("唯一值:", s_unique.unique())
# value_counts() - 统计值的出现次数
print("值的计数:")
print(s_unique.value_counts())
# describe() - 生成统计摘要
print("s_stats的统计摘要:")
print(s_stats.describe())
# 输出结果:
# 唯一值: [1 2 3]
# 值的计数:
# 3    3
# 2    2
# 1    1
# dtype: int64
# s_stats的统计摘要:
# count    5.000000
# mean    30.000000
# std     15.811388
# min     10.000000
# 25%     20.000000
# 50%     30.000000
# 75%     40.000000
# max     50.000000
# dtype: float64
print(50 * "*")


# 2.6 Series 的缺失值处理
# Pandas 使用NaN（Not a Number）表示缺失值，这是数据分析中的常见情况
# 缺失值的创建与识别
# 创建包含缺失值的Series
s_missing = pd.Series([10, 20, np.nan, 40, np.nan], index=['a', 'b', 'c', 'd', 'e'])
print("s_missing:")
print(s_missing)
# 检查缺失值
print("检查缺失值（isna）:")
print(s_missing.isna())
print("检查非缺失值（notna）:")
print(s_missing.notna())
# 输出结果:
# s_missing:
# a    10.0
# b    20.0
# c     NaN
# d    40.0
# e     NaN
# dtype: float64
# 检查缺失值（isna）:
# a    False
# b    False
# c     True
# d    False
# e     True
# dtype: bool
# 检查非缺失值（notna）:
# a     True
# b     True
# c    False
# d     True
# e    False
# dtype: bool
print(50 * ".")

# 缺失值的处理方法
# dropna() - 删除包含缺失值的行
print("删除缺失值后:")
print(s_missing.dropna())
# fillna() - 填充缺失值
print("用0填充缺失值:")
print(s_missing.fillna(0))
print("用前向值填充（ffill）:")
print(s_missing.fillna(method='ffill'))
print("用后向值填充（bfill）:")
print(s_missing.fillna(method='bfill'))
# 输出结果:
# 删除缺失值后:
# a    10.0
# b    20.0
# d    40.0
# dtype: float64
# 用0填充缺失值:
# a    10.0
# b    20.0
# c     0.0
# d    40.0
# e     0.0
# dtype: float64
# 用前向值填充（ffill）:
# a    10.0
# b    20.0
# c    20.0
# d    40.0
# e    40.0
# dtype: float64
# 用后向值填充（bfill）:
# a    10.0
# b    20.0
# c    40.0
# d    40.0
# e    40.0
# dtype: float64
print(50 * "*")


# 2.7 Series 的字符串操作
# 当 Series 包含字符串时，可以使用.str属性进行字符串操作
s_str = pd.Series(['Hello', 'World', 'Python', 'Pandas'])
print("转换为大写:")
print(s_str.str.upper())
print("转换为小写:")
print(s_str.str.lower())
print("包含'P'的元素:")
print(s_str[s_str.str.contains('P')])
print("以'H'开头的元素:")
print(s_str[s_str.str.startswith('H')])
# 输出结果:
# 转换为大写:
# 0    HELLO
# 1    WORLD
# 2    PYTHON
# 3    PANDAS
# dtype: object
# 转换为小写:
# 0    hello
# 1    world
# 2    python
# 3    pandas
# dtype: object
# 包含'P'的元素:
# 2    Python
# 3    Pandas
# dtype: object
# 以'H'开头的元素:
# 0    Hello
# dtype: object
print(50 * "*")

# 验证输出及知识补充
#################################################################################


# Pandas DataFrame 基础
# 3.1 DataFrame 的创建
# DataFrame 是 Pandas 的核心二维数据结构，可以理解为 “带标签的二维表格” 或 “由多个同索引 Series 组成的字典”

# 从字典创建
# 最常用的创建方式是从字典创建 DataFrame
# 从字典创建DataFrame
data = {
   'Name': ['Alice', 'Bob', 'Charlie', 'David'],
   'Age': [25, 30, 35, 40],
   'Score': [85.5, 90.0, 78.5, 88.0],
   'City': ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen']
}
df1 = pd.DataFrame(data)
print("df1:")
print(df1)
# 输出结果:
#      Name  Age  Score      City
# 0    Alice   25   85.5   Beijing
# 1      Bob   30   90.0  Shanghai
# 2  Charlie   35   78.5  Guangzhou
# 3    David   40   88.0  Shenzhen
print(50 * ".")

# 从列表的字典创建
data_list = [
   {'Name': 'Alice', 'Age': 25, 'Score': 85.5, 'City': 'Beijing'},
   {'Name': 'Bob', 'Age': 30, 'Score': 90.0, 'City': 'Shanghai'},
   {'Name': 'Charlie', 'Age': 35, 'Score': 78.5, 'City': 'Guangzhou'},
   {'Name': 'David', 'Age': 40, 'Score': 88.0, 'City': 'Shenzhen'}
]
df2 = pd.DataFrame(data_list)
print("df2:")
print(df2)
# 输出结果与df1相同
print(50 * ".")

# 从 Series 字典创建
s_name = pd.Series(['Alice', 'Bob', 'Charlie', 'David'], name='Name')
s_age = pd.Series([25, 30, 35, 40], name='Age')
s_score = pd.Series([85.5, 90.0, 78.5, 88.0], name='Score')
s_city = pd.Series(['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen'], name='City')
df3 = pd.DataFrame({
   'Name': s_name,
   'Age': s_age,
   'Score': s_score,
   'City': s_city
})
print("df3:")
print(df3)
# 输出结果与df1相同
print(50 * ".")

# 从NumPy数组创建
np_data = np.array([
   [25, 85.5, 'Beijing'],
   [30, 90.0, 'Shanghai'],
   [35, 78.5, 'Guangzhou'],
   [40, 88.0, 'Shenzhen']
])
df4 = pd.DataFrame(
   np_data,
   index=['Alice', 'Bob', 'Charlie', 'David'],
   columns=['Age', 'Score', 'City']
)
print("df4:")
print(df4)
# 输出结果:
#          Age  Score      City
# Alice    25   85.5   Beijing
# Bob      30   90.0  Shanghai
# Charlie  35   78.5  Guangzhou
# David    40   88.0  Shenzhen
print(50 * ".")

# 创建空 DataFrame
df_empty = pd.DataFrame(columns=['Name', 'Age', 'Score'])
print("空DataFrame:")
print(df_empty)
# 输出结果:
# Empty DataFrame
# Columns: [Name, Age, Score]
# Index: []
print(50 * "*")


# 3.2 DataFrame 的基本属性
# DataFrame 具有丰富的属性来描述其结构和数据
# 维度信息
# shape: 返回（行数，列数）的元组
# ndim: 返回维度数
# size: 返回元素总数
print(f"df1的形状: {df1.shape}")
print(f"df1的维度: {df1.ndim}")
print(f"df1的元素总数: {df1.size}")
# 输出结果:
# df1的形状: (4, 4)
# df1的维度: 2
# df1的元素总数: 16
print(50 * ".")

# 索引和列
# index: 获取行索引
# columns: 获取列索引
print("df1的行索引:")
print(df1.index)
print("df1的列索引:")
print(df1.columns)
# 输出结果:
# df1的行索引: RangeIndex(start=0, stop=4, step=1)
# df1的列索引: Index(['Name', 'Age', 'Score', 'City'], dtype='object')
print(50 * ".")

# 数据类型
# dtypes: 获取各列的数据类型
# info(): 获取数据结构信息
print("df1各列的数据类型:")
print(df1.dtypes)
print("df1的数据结构信息:")
df1.info()
# 输出结果:
# df1各列的数据类型:
# Name      object
# Age       int64
# Score    float64
# City      object
# dtype: object
# df1的数据结构信息:
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 4 entries, 0 to 3
# Data columns (total 4 columns):
#  #   Column  Non-Null Count  Dtype
#  --  ------  --------------  -----
#  0   Name    4 non-null      object
#  1   Age     4 non-null      int64
#  2   Score   4 non-null      float64
#  3   City    4 non-null      object
# dtypes: float64(1), int64(1), object(2)
# memory usage: 208.0+ bytes
print(50 * ".")

# 值的获取
# values: 获取 DataFrame 的值（返回 NumPy 数组）
# to_numpy(): 转换为 NumPy 数组
print("df1的值（NumPy数组）:")
print(df1.values)
print(f"类型: {type(df1.values)}")
print("df1转换为NumPy数组:")
np_array = df1.to_numpy()
print(np_array)
# 输出结果:
# df1的值（NumPy数组）:
# array([['Alice', 25, 85.5, 'Beijing'],
#        ['Bob', 30, 90.0, 'Shanghai'],
#        ['Charlie', 35, 78.5, 'Guangzhou'],
#        ['David', 40, 88.0, 'Shenzhen']], dtype=object)
# 类型: <class 'numpy.ndarray'>
print(50 * "*")


# 3.3 DataFrame 的数据选择与索引
# DataFrame 的索引系统是其强大功能的核心，支持多种灵活的数据选择方式

# 列选择
# 最简单的列选择方式
print(df1)
print("选择'Age'列:")
print(df1['Age'])
print(f"类型: {type(df1['Age'])}")
print("选择'Score'列:")
print(df1.Score)  # 当列名是合法标识符时可以使用点操作
# 输出结果:
# 选择'Age'列:
# 0    25
# 1    30
# 2    35
# 3    40
# Name: Age, dtype: int64
# 类型: <class 'pandas.core.series.Series'>
print(50 * ".")

# 选择多列
print("选择'Name'和'Score'列:")
print(df1[['Name', 'Score']])
print(f"类型: {type(df1[['Name', 'Score']])}")
# 输出结果:
# 选择'Name'和'Score'列:
#      Name  Score
# 0    Alice   85.5
# 1      Bob   90.0
# 2  Charlie   78.5
# 3    David   88.0
# 类型: <class 'pandas.core.frame.DataFrame'>
print(50 * ".")

# 行选择 - loc 与 iloc
# 基于标签的行选择（.loc[]）
print("选择索引为1的行（loc）:")
print(df1.loc[1])
print("选择索引为0到2的行（loc，包含结束）:")
print(df1.loc[0:2])
print("选择索引为[0,2,3]的行:")
print(df1.loc[[0, 2, 3]])
# 输出结果:
# 选择索引为1的行（loc）:
# Name      Bob
# Age       30
# Score     90.0
# City    Shanghai
# Name: 1, dtype: object
# 选择索引为0到2的行（loc，包含结束）:
#      Name  Age  Score      City
# 0    Alice   25   85.5   Beijing
# 1      Bob   30   90.0  Shanghai
# 2  Charlie   35   78.5  Guangzhou
# 选择索引为[0,2,3]的行:
#      Name  Age  Score      City
# 0    Alice   25   85.5   Beijing
# 2  Charlie   35   78.5  Guangzhou
# 3    David   40   88.0  Shenzhen
print(50 * ".")

# 基于位置的行选择（.iloc[]）
print("选择第2行（iloc，位置索引）:")
print(df1.iloc[1])
print("选择第0到1行（iloc，不包含结束）:")
print(df1.iloc[0:2])
print("选择第0、2、3行:")
print(df1.iloc[[0, 2, 3]])
# 输出结果:
# 选择第2行（iloc，位置索引）:
# Name      Bob
# Age       30
# Score     90.0
# City    Shanghai
# Name: 1, dtype: object
# 选择第0到1行（iloc，不包含结束）:
#      Name  Age  Score      City
# 0    Alice   25   85.5   Beijing
# 1      Bob   30   90.0  Shanghai
print(50 * ".")

# 行列混合选择
# loc[]和.iloc[]都支持行列混合选择
print("选择第0-1行，'Name'和'Age'列（loc）:")
print(df1.loc[0:1, ['Name', 'Age']])
print("选择第0-1行，前2列（iloc）:")
print(df1.iloc[0:2, 0:2])
print("选择第0行，'Score'列（loc）:")
print(df1.loc[0, 'Score'])
print("选择第0行，第2列（iloc）:")
print(df1.iloc[0, 2])
# 输出结果:
# 选择第0-1行，'Name'和'Age'列（loc）:
#      Name  Age
# 0    Alice   25
# 1      Bob   30
# 选择第0-1行，前2列（iloc）:
#      Name  Age
# 0    Alice   25
# 1      Bob   30
# 选择第0行，'Score'列（loc）:
# 85.5
# 选择第0行，第2列（iloc）:
# 85.5
print(50 * ".")

# 布尔索引
# 这是最强大的索引方式之一
print("年龄大于30岁的行:")
print(df1[df1['Age'] > 30])
print("成绩在80-90之间的行:")
print(df1[(df1['Score'] >= 80) & (df1['Score'] <= 90)])
print("来自北京或上海的行:")
print(df1[df1['City'].isin(['Beijing', 'Shanghai'])])
# 输出结果:
# 年龄大于30岁的行:
#      Name  Age  Score      City
# 2  Charlie   35   78.5  Guangzhou
# 3    David   40   88.0  Shenzhen
# 成绩在80-90之间的行:
#      Name  Age  Score      City
# 0    Alice   25   85.5   Beijing
# 1      Bob   30   90.0  Shanghai
# 3    David   40   88.0  Shenzhen
# 来自北京或上海的行:
#      Name  Age  Score      City
# 0    Alice   25   85.5   Beijing
# 1      Bob   30   90.0  Shanghai
print(50 * "*")


# 3.4 DataFrame 的基本操作
# 新增列
df1['Gender'] = ['F', 'M', 'M', 'M']
print("新增Gender列后:")
print(df1)
# 基于现有列计算新增列
df1['Score_Level'] = df1['Score'].apply(lambda x: 'A' if x >= 90 else ('B' if x >= 80 else 'C'))
print("新增Score_Level列:")
print(df1)
# 输出结果:
#      Name  Age  Score      City Gender
# 0    Alice   25   85.5   Beijing      F
# 1      Bob   30   90.0  Shanghai      M
# 2  Charlie   35   78.5  Guangzhou      M
# 3    David   40   88.0  Shenzhen      M
# 新增Score_Level列:
#      Name  Age  Score      City Gender Score_Level
# 0    Alice   25   85.5   Beijing      F          B
# 1      Bob   30   90.0  Shanghai      M          A
# 2  Charlie   35   78.5  Guangzhou      M          C
# 3    David   40   88.0  Shenzhen      M          B
print(50 * ".")

# 修改列
# 修改列值
df1['Score'] = df1['Score'] + 1
print("Score列加1后:")
print(df1)
# 修改特定行的值
df1.loc[0, 'Score'] = 86.5
print("修改第0行Score值:")
print(df1)
# 批量修改
df1['Age'] = df1['Age'] + 1
print("Age列加1后:")
print(df1)
# 输出结果:
# Score列加1后:
#      Name  Age  Score      City Gender Score_Level
# 0    Alice   25   86.5   Beijing      F          B
# 1      Bob   30   91.0  Shanghai      M          A
# 2  Charlie   35   79.5  Guangzhou      M          C
# 3    David   40   89.0  Shenzhen      M          B
# 修改第0行Score值:
#      Name  Age  Score      City Gender Score_Level
# 0    Alice   25   86.5   Beijing      F          B
# 1      Bob   30   91.0  Shanghai      M          A
# 2  Charlie   35   79.5  Guangzhou      M          C
# 3    David   40   89.0  Shenzhen      M          B
# Age列加1后:
#      Name  Age  Score      City Gender Score_Level
# 0    Alice   26   86.5   Beijing      F          B
# 1      Bob   31   91.0  Shanghai      M          A
# 2  Charlie   36   79.5  Guangzhou      M          C
# 3    David   41   89.0  Shenzhen      M          B
print(50 * ".")

# 删除列
# 删除列（方法1: 使用del）
del df1['Score_Level']
print("删除Score_Level列后:")
print(df1)
# 删除列（方法2: 使用pop）
gender = df1.pop('Gender')
print("删除Gender列（使用pop）:")
print(df1)
print("被删除的Gender列:")
print(gender)
# 输出结果:
# 删除Score_Level列后:
#      Name  Age  Score      City Gender
# 0    Alice   26   86.5   Beijing      F
# 1      Bob   31   91.0  Shanghai      M
# 2  Charlie   36   79.5  Guangzhou      M
# 3    David   41   89.0  Shenzhen      M
# 删除Gender列（使用pop）:
#      Name  Age  Score      City
# 0    Alice   26   86.5   Beijing
# 1      Bob   31   91.0  Shanghai
# 2  Charlie   36   79.5  Guangzhou
# 3    David   41   89.0  Shenzhen
# 被删除的Gender列:
# 0    F
# 1    M
# 2    M
# 3    M
# Name: Gender, dtype: object
print(50 * ".")

# 重命名列
# 重命名列（方法1: rename）
df_renamed = df1.rename(columns={
   'Name': 'Full_Name',
   'Age': 'Years_Old'
})
print("重命名列（方法1）:")
print(df_renamed)
# 重命名列（方法2: 直接修改columns属性）
df1.columns = ['Full_Name', 'Years_Old', 'Score_Point', 'Location']
print("重命名列（方法2）:")
print(df1)
# 输出结果:
# 重命名列（方法1）:
#      Full_Name  Age  Score      City
# 0    Alice   26   86.5   Beijing
# 1      Bob   31   91.0  Shanghai
# 2  Charlie   36   79.5  Guangzhou
# 3    David   41   89.0  Shenzhen
# 重命名列（方法2）:
#      Full_Name  Years_Old  Score_Point  Location
# 0    Alice        26        86.5    Beijing
# 1      Bob         31        91.0   Shanghai
# 2  Charlie       36        79.5   Guangzhou
# 3    David       41        89.0   Shenzhen
print(50 * "*")


# 3.5 DataFrame 的运算操作
# 算术运算
# DataFrame 支持向量化运算，运算会按元素进行
df_math = pd.DataFrame({
   'A': [1, 2, 3, 4],
   'B': [10, 20, 30, 40],
   'C': [100, 200, 300, 400]
})
print("df_math:")
print(df_math)
print("df_math + 5:")
print(df_math + 5)
print("df_math * 2:")
print(df_math * 2)
print("df_math['A'] + df_math['B']:")
print(df_math['A'] + df_math['B'])
# 输出结果:
# df_math:
#    A   B    C
# 0  1  10  100
# 1  2  20  200
# 2  3  30  300
# 3  4  40  400
# df_math + 5:
#    A   B    C
# 0  6  15  105
# 1  7  25  205
# 2  8  35  305
# 3  9  45  405
# df_math * 2:
#    A    B     C
# 0  2   20   200
# 1  4   40   400
# 2  6   60   600
# 3  8   80   800
# df_math['A'] + df_math['B']:
# 0    11
# 1    22
# 2    33
# 3    44
# Name: A, dtype: int64
print(50 * ".")

# 比较运算
print("df_math > 10:")
print(df_math > 10)
print("df_math[df_math > 10]:")
print(df_math[df_math > 10])
print("df_math['B'] >= 20:")
print(df_math['B'] >= 20)
# 输出结果:
# df_math > 10:
#        A      B      C
# 0  False   True   True
# 1  False   True   True
# 2  False   True   True
# 3  False   True   True
# df_math[df_math > 10]:
#      A     B      C
# 0  NaN  10.0  100.0
# 1  NaN  20.0  200.0
# 2  NaN  30.0  300.0
# 3  NaN  40.0  400.0
# df_math['B'] >= 20:
# 0    False
# 1     True
# 2     True
# 3     True
# dtype: bool
print(50 * ".")

# 广播运算
# 类似 NumPy 的广播机制，Pandas 也支持广播运算
# 创建一个Series，用于广播运算
s_broadcast = pd.Series([100, 200, 300], index=['A', 'B', 'C'])
print("df_math + s_broadcast:")
print(df_math + s_broadcast)
# 输出结果:
# df_math + s_broadcast:
#     A     B      C
# 0  101   110    NaN
# 1  102   120    NaN
# 2  103   130    NaN
# 3  104   140    NaN
# 注意: 由于索引不匹配，C列无法进行运算
print(50 * "*")


# 3.6 DataFrame 的统计方法
# DataFrame 提供了丰富的统计方法
# 基本统计方法
df_stats = pd.DataFrame({
   'A': [10, 20, 30, 40],
   'B': [100, 200, 300, 400],
   'C': [1000, 2000, 3000, 4000]
})
print("df_stats的统计摘要:")
print(df_stats.describe())
print("每列的和:")
print(df_stats.sum())
print("每列的均值:")
print(df_stats.mean())
print("每列的最大值:")
print(df_stats.max())
print("每列的最小值:")
print(df_stats.min())
print("每列的标准差:")
print(df_stats.std())
# 输出结果:
# df_stats的统计摘要:
#              A        B         C
# count   4.000000  4.000000   4.000000
# mean   25.000000  250.000000  2500.000000
# std    11.180340  111.803401  1118.034013
# min    10.000000  100.000000  1000.000000
# 25%    17.500000  175.000000  1750.000000
# 50%    25.000000  250.000000  2500.000000
# 75%    32.500000  325.000000  3250.000000
# max    40.000000  400.000000  4000.000000
# 每列的和:
# A     100
# B    1000
# C   10000
# dtype: int64
# 每列的均值:
# A      25.0
# B     250.0
# C    2500.0
# dtype: float64
print(50 * ".")

# 按轴运算
print("按行求和（axis=1）:")
print(df_stats.sum(axis=1))
print("每行的均值（axis=1）:")
print(df_stats.mean(axis=1))
# 输出结果:
# 按行求和（axis=1）:
# 0    1110
# 1    2220
# 2    3330
# 3    4440
# dtype: int64
# 每行的均值（axis=1）:
# 0    370.0
# 1    740.0
# 2   1110.0
# 3   1480.0
# dtype: float64
print(50 * ".")

# 其他统计方法
print("数据个数（非缺失值）:")
print(df_stats.count())
print("中位数:")
print(df_stats.median())
print("唯一值（对于非数值列）:")
df_str = pd.DataFrame({
   'City': ['Beijing', 'Shanghai', 'Beijing', 'Shenzhen']
})
print(df_str['City'].unique())
print("值的计数:")
print(df_str['City'].value_counts())
# 输出结果:
# 数据个数（非缺失值）:
# A    4
# B    4
# C    4
# dtype: int64
# 中位数:
# A      25.0
# B     250.0
# C    2500.0
# dtype: float64
# 唯一值（对于非数值列）:
# ['Beijing' 'Shanghai' 'Shenzhen']
# 值的计数:
# Beijing      2
# Shanghai     1
# Shenzhen     1
# Name: City, dtype: int64


# 3.7 DataFrame 的排序
# 按值排序
df_sort = pd.DataFrame({
   'Name': ['Charlie', 'Alice', 'David', 'Bob'],
   'Age': [35, 25, 40, 30],
   'Score': [78.5, 85.5, 88.0, 90.0]
})
print("原始df_sort:")
print(df_sort)
print("按'Age'列升序排序:")
print(df_sort.sort_values('Age'))
print("按'Age'列降序排序:")
print(df_sort.sort_values('Age', ascending=False))
print("按'Score'列升序排序:")
print(df_sort.sort_values('Score'))
# 输出结果:
# 原始df_sort:
#      Name  Age  Score
# 0  Charlie   35   78.5
# 1    Alice   25   85.5
# 2    David   40   88.0
# 3      Bob   30   90.0
# 按'Age'列升序排序:
#      Name  Age  Score
# 1    Alice   25   85.5
# 3      Bob   30   90.0
# 0  Charlie   35   78.5
# 2    David   40   88.0
# 按'Age'列降序排序:
#      Name  Age  Score
# 2    David   40   88.0
# 0  Charlie   35   78.5
# 3      Bob   30   90.0
# 1    Alice   25   85.5
# 按'Score'列升序排序:
#      Name  Age  Score
# 0  Charlie   35   78.5
# 1    Alice   25   85.5
# 2    David   40   88.0
# 3      Bob   30   90.0
print(50 * ".")

# 按多列排序
print("按'Age'升序，'Score'降序排序:")
print(df_sort.sort_values(['Age', 'Score'], ascending=[True, False]))
print("按'Age'降序，'Score'升序排序:")
print(df_sort.sort_values(['Age', 'Score'], ascending=[False, True]))
# 输出结果:
# 按'Age'升序，'Score'降序排序:
#      Name  Age  Score
# 1    Alice   25   85.5
# 3      Bob   30   90.0
# 0  Charlie   35   78.5
# 2    David   40   88.0
# 按'Age'降序，'Score'升序排序:
#      Name  Age  Score
# 2    David   40   88.0
# 0  Charlie   35   78.5
# 3      Bob   30   90.0
# 1    Alice   25   85.5
print(50 * ".")

# 按索引排序
print("按索引排序:")
print(df_sort.sort_index())
# 输出结果:
# 按索引排序:
#      Name  Age  Score
# 0  Charlie   35   78.5
# 1    Alice   25   85.5
# 2    David   40   88.0
# 3      Bob   30   90.0