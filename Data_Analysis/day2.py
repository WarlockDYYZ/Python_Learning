# Pandas Series
# Pandas Series是一个一维带标签的数组结构，由数据和相关的索引（标签）组成。它可以看作是一个 “带索引的列表” 或 “有序字典”，具有以下核心特点：
# 标签索引：与 NumPy 数组的隐式整数索引不同，Series 具有显式的标签索引，大大提高了数据的可读性和可操作性。
# 同质数据类型：Series 中的元素必须是相同的数据类型，这与列表不同（列表元素可以是不同类型），但与 NumPy 数组相同。
# 灵活的索引类型：索引可以是整数、字符串、日期等任意不可变类型，且支持非唯一索引。
# 类似字典的操作：可以像字典一样通过标签访问元素，同时保留了数组的向量化运算特性。
# 自动对齐：在运算时会自动根据索引进行数据对齐，这是与 NumPy 数组的重要区别。

# Pandas Series 可以从多种数据源创建，以下是常见的创建方式
# 从列表创建 Series
import pandas as pd
import numpy as np
# 从列表创建，使用默认整数索引
s1 = pd.Series([10, 20, 30, 40, 50])
print("Series s1（默认索引）：")
print(s1)
print("索引：", s1.index)  # RangeIndex(start=0, stop=5, step=1)
print("数据：", s1.values)  # [10 20 30 40 50]
# 从列表创建，指定自定义索引
s2 = pd.Series([88, 92, 79, 95], index=['张三', '李四', '王五', '赵六'])
print("Series s2（自定义索引）：")
print(s2)
# 从列表创建，指定数据类型
s3 = pd.Series([1, 2, 3, 4], dtype='float32')
print("Series s3（指定dtype）：")
print(s3)
print(50 * "=")

# 从字典创建 Series
# 从字典创建，键作为索引
d = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
s4 = pd.Series(d)
print("从字典创建：")
print(s4)
# 从字典创建，指定索引（会筛选字典中存在的键）
s5 = pd.Series(d, index=['b', 'c', 'e'])
print("指定索引筛选：")
print(s5)  # e不存在，值为NaN
print(50 * "=")

# 从标量值创建 Series
# 从标量值创建，必须指定索引
s6 = pd.Series(5.0, index=['a', 'b', 'c', 'd', 'e'])
print("从标量创建：")
print(s6)  # 所有元素都是5.0
# 从NumPy数组创建
arr = np.array([1, 2, 3, 4, 5])
s7 = pd.Series(arr)
print("从NumPy数组创建：")
print(s7)
print(50 * "=")

# Pandas Series 的索引与切片
# Series 的索引机制比 NumPy 数组更加灵活，支持位置索引和标签索引两种方式
# 1. 基本索引操作
s = pd.Series([10, 20, 30, 40, 50], index=['a', 'b', 'c', 'd', 'e'])
print("Series：")
print(s)
# 通过标签索引访问
print("标签索引：")
print(s['a'])  # 10
print(s['c'])  # 30
print(s[['a', 'c', 'e']])  # 多个标签
# 通过位置索引访问
print("位置索引：")
print(s.iloc[0])  # 10
print(s.iloc[2])  # 30
print(s.iloc[[0, 2, 4]])  # 多个位置
print(50 * "=")

# 2. 使用 loc() 和 iloc() 进行索引
# 最推荐的索引方式，避免混淆位置和标签
print("使用loc（标签索引）：")
print(s.loc['a'])  # 10
print(s.loc['a':'c'])  # 标签切片，包含结束标签（闭区间）
print("使用iloc（位置索引）：")
print(s.iloc[0])  # 10
print(s.iloc[0:2])  # 位置切片，不包含结束索引（开区间）
print(50 * "=")

# 3. 切片操作的特殊之处
# 标签切片是闭区间（包含起始和结束标签），而位置切片是开区间（不包含结束索引）
s = pd.Series([1, 2, 3, 4, 5], index=['a', 'b', 'c', 'd', 'e'])
print("标签切片（闭区间）：")
print(s['a':'c'])  # 输出 a b c 三个元素
print("位置切片（开区间）：")
print(s[0:2])  # 输出第0和第1个元素
print(50 * "=")

# 4. 布尔索引
s = pd.Series([10, 20, 30, 40, 50])
print("布尔索引：")
print(s[s > 30])  # 大于30的元素
print(s[(s % 2 == 0) & (s > 20)])  # 偶数且大于20
# 多个条件组合
print("复合条件：")
mask1 = s > 25
mask2 = s < 45
print(s[mask1 & mask2])
print(50 * "=")

# Pandas Series 的运算操作
# Series 的运算操作具有强大的自动对齐功能，这是与 NumPy 数组的重要区别
# 1. 算术运算
s1 = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
s2 = pd.Series([10, 20, 30, 40], index=['a', 'b', 'c', 'd'])
print("Series s1：", s1)
print("Series s2：", s2)
# 加法运算
print("加法运算：")
print(s1 + s2)
# 减法运算
print("减法运算：")
print(s1 - s2)
# 乘法运算
print("乘法运算：")
print(s1 * s2)
# 除法运算
print("除法运算：")
print(s1 / s2)

# 2. 自动对齐机制
# 当两个 Series 的索引不完全相同时，Pandas 会自动对齐索引，缺失的值用 NaN 表示
# Pandas 会自动对齐索引，缺失的值用 NaN 表示
s3 = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
s4 = pd.Series([10, 20, 30, 40], index=['b', 'c', 'd', 'e'])
print("Series s3：", s3)
print("Series s4：", s4)
print("自动对齐相加：")
print(s3 + s4)  # a和e位置会出现NaN
print(50 * "=")

# 3. 与标量运算
s = pd.Series([10, 20, 30, 40])
print("Series：", s)
# 与标量相加
print("加标量：", s + 5)
# 与标量相乘
print("乘标量：", s * 2)
# 其他运算
print("其他运算：")
print(s - 3)
print(s / 10)
print(s ** 2)
print(50 * "=")

# 4. 与 NumPy 数组运算
s = pd.Series([1, 2, 3, 4])
arr = np.array([10, 20, 30, 40])
print("Series：", s)
print("NumPy数组：", arr)
# Series与NumPy数组运算
print("运算结果：")
print(s + arr)  # 按位置相加
print(s * arr)  # 按位置相乘
print(50 * "=")

# 5. 统计运算
# Series 提供了丰富的统计函数
s = pd.Series([10, 20, 30, 40, 50])
print("Series统计：")
print("求和：", s.sum())
print("平均值：", s.mean())
print("最大值：", s.max())
print("最小值：", s.min())
print("标准差：", s.std())
# 总体方差，适用于你拥有全部数据的情况，计算时除以数据总个数 n
# 如果这组数据是从一个更大的总体中抽取的样本，那么计算样本方差时，分母应为 n-1
# 该方差即为样本方差
print("方差：", s.var())
print("中位数：", s.median())
print("元素个数：", s.count())
print(50 * "=")

# 3.5 Pandas Series 的其他重要操作
# 1. 索引操作
s = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
print("原始Series：", s)
# 修改索引
s.index = ['x', 'y', 'z']
print("修改索引后：", s)
# 重命名索引（inplace=False，返回新对象）
s2 = s.rename(index={'x': 'A', 'y': 'B'})
print("重命名部分索引：", s2)
# 重置索引（会添加一个新的默认索引列）
s3 = s.reset_index()
print("重置索引：")
print(s3)
print(50 * "=")

# 2. 数据对齐操作
s1 = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
s2 = pd.Series([10, 20, 30], index=['c', 'b', 'a'])
print("s1：", s1)
print("s2：", s2)
# 使用align方法进行对齐
s1_aligned, s2_aligned = s1.align(s2)
print("对齐后：")
print("s1对齐后：", s1_aligned)
print("s2对齐后：", s2_aligned)
print(50 * "=")

# 3. 缺失值处理
s = pd.Series([1, 2, None, 4, np.nan, 6])
print("包含缺失值的Series：", s)
# 检测缺失值
print("检测缺失值：")
print(s.isna())  # True表示缺失
print(s.notna())  # False表示缺失
# 删除缺失值
s_clean = s.dropna()
print("删除缺失值后：", s_clean)
# 填充缺失值
s_filled = s.fillna(0)  # 用0填充
print("填充缺失值（0）：", s_filled)
s_filled2 = s.fillna(method='ffill')  # 用前值填充
print("前向填充（ffill）：", s_filled2)
print(50 * "=")

# Pandas DataFrame 是一个 二维表格型数据结构 ，可以看作是 Series 的容器，由多个 Series 按行组合而成
# 1. 二维表格结构：由行索引（index）、列索引（columns）和数据区域（values）三部分组成，类似 Excel 表格或数据库表(38)。
# 2. 异构数据类型：每列可以存储不同的数据类型（如整数、字符串、浮点数、日期等），但每列内部的数据类型必须相同(37)。
# 3. 行列标签：既有行索引（row labels）又有列索引（column labels），提供了强大的标签化数据操作能力(38)。
# 4. 数据对齐：在运算时会自动对齐行和列索引，这一特性贯穿整个 Pandas 库(74)。
# 5. 灵活的操作：支持类似字典的列操作和类似数组的行操作，提供了丰富的数据处理方法。
# Pandas DataFrame 的创建方法
# 1. 从字典（列表作为值）创建
data1 = {
   '姓名': ['张三', '李四', '王五', '赵六'],
   '年龄': [20, 21, 19, 22],
   '性别': ['男', '女', '男', '女'],
   '成绩': [85, 92, 78, 88]
}
df1 = pd.DataFrame(data1)
print("从字典（列表）创建：")
print(df1)
# 从字典（Series作为值）创建
data2 = {
   '姓名': pd.Series(['张三', '李四', '王五'], index=[0, 1, 2]),
   '年龄': pd.Series([20, 21, 19], index=[0, 1, 2]),
   '成绩': pd.Series([85, 92, 78], index=[0, 1, 2])
}
df2 = pd.DataFrame(data2)
print("从字典（Series）创建：")
print(df2)
# 从字典创建，指定列顺序
df3 = pd.DataFrame(data1, columns=['姓名', '年龄', '成绩'])
print("指定列顺序：")
print(df3)

# 2. 从二维数组创建 DataFrame
# 从NumPy二维数组创建
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
df4 = pd.DataFrame(arr, index=['a', 'b', 'c'], columns=['X', 'Y', 'Z'])
print("从二维数组创建：")
print(df4)
# 从列表的列表创建
list_of_lists = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
df5 = pd.DataFrame(list_of_lists, columns=['A', 'B', 'C'])
print("\n从列表的列表创建：")
print(df5)

# 3. 从结构化数组创建
# 创建结构化数组
# i4 = int32, f4 = float32, a10 = 长度为 10 的字节字符串
data = np.zeros(2, dtype=[('A', 'i4'), ('B', 'f4'), ('C', 'a10')])
data[0] = (1, 2.0, 'Hello')
data[1] = (2, 3.0, 'World')
df6 = pd.DataFrame(data)
print("从结构化数组创建：")
print(df6)
print(50 * "=")

# 4. 从其他 DataFrame 或 Series 创建
# 从Series创建（会成为DataFrame的一列）
s = pd.Series([1, 2, 3, 4], name='Numbers')
df7 = pd.DataFrame(s)
print("从Series创建：")
print(df7)
# 从多个Series创建
s1 = pd.Series([1, 2, 3], name='A')
s2 = pd.Series([4, 5, 6], name='B')
print("原输出形状：")
print(pd.DataFrame([s1, s2]))
df8 = pd.DataFrame([s1, s2]).T
print("从多个Series创建：(T 转置以获得正确的形状)")
print(df8)
print(50 * "=")

# 5. 从字典列表创建
# 从字典列表创建
data_list = [
   {'姓名': '张三', '年龄': 20, '成绩': 85},
   {'姓名': '李四', '年龄': 21, '成绩': 92},
   {'姓名': '王五', '年龄': 19, '成绩': 78}
]
df9 = pd.DataFrame(data_list)
print("从字典列表创建：")
print(df9)
print(50 * "=")

# 4.3 Pandas DataFrame 的索引与切片
# DataFrame 的索引机制是其最强大的特性之一，提供了多种灵活的方式来访问和操作数据
# 1. 基本索引操作
# 创建示例DataFrame
df = pd.DataFrame({
   'A': [1, 2, 3, 4],
   'B': [10, 20, 30, 40],
   'C': ['a', 'b', 'c', 'd']
}, index=['row1', 'row2', 'row3', 'row4'])
# index 代表行
print("示例DataFrame：")
print(df)

# 列索引（类似字典操作）
print("列索引操作：")
print("选择列'A'：")
print(df['A'])  # 返回Series
print("选择多列：")
print(df[['A', 'B']])  # 返回DataFrame

# 行切片（直接使用[]）
print("行切片：")
print("前两行：")
print(df[:2])  # 基于位置的切片
print("指定索引的行：")
print(df['row2':'row4'])  # 基于标签的切片（闭区间）
print(50 * "=")

# 2. 使用 loc 和 iloc 进行高级索引
# DataFrame 索引的标准方法，强烈推荐使用
print("使用loc（标签索引）：")
print("选择row2：")
print(df.loc['row2'])  # 返回Series
print("选择row2和row4的A、B列：")
# 逐一选择“,”, 切片(范围)":"
print(df.loc[['row2', 'row4'], ['A', 'B']])
print("选择row2到row4的所有列：")
print(df.loc['row2':'row4', :])
print("使用iloc（位置索引）：")
# 选择规则同上，单个参数传入，默认操作行
print("选择第2行：")
print(df.iloc[1])  # 注意：索引从0开始
print("选择第2行第1、2列：")
print(df.iloc[1, [0, 1]])
print("选择第2-4行的所有列：")
print(df.iloc[1:4, :])
print(50 * "=")

# 3. 布尔索引
print("布尔索引：")
print("选择A列大于2的行：")
mask = df['A'] > 2
print(df[mask])
print("选择B列等于20或40的行：")
# .isin（）
# Whether elements in Series are contained in values.
# Return a boolean Series showing whether each element in the Series
# matches an element in the passed sequence of values exactly.
# 上面是官方文档的解释，大概能看懂，我又查了一下
# 判断 Series 中的元素是否包含在指定值集合内
# 返回一个布尔类型的 Series，表明原 Series 中的每个元素是否精确匹配传入的值序列中的某个元素
# df[mask2], 根据返回的布尔类型的 Series, 筛选值为True的行
mask2 = df['B'].isin([20, 40])
print(df[mask2])
print("组合条件：A>2且B<40：")
mask3 = (df['A'] > 2) & (df['B'] < 40)
print(df[mask3])
print(50 * "=")

# 4. 按条件筛选和修改
print("条件筛选和修改：")
print("原始数据：")
print(df)
# 将A列大于2的行的B列设置为0
df.loc[df['A'] > 2, 'B'] = 0
print("修改后：")
print(df)
print(50 * "=")

# 4.4 Pandas DataFrame 的运算操作
# DataFrame 的运算操作同样具有强大的自动对齐功能，支持多种运算方式
# 1. 算术运算
df1 = pd.DataFrame({
   'A': [1, 2, 3],
   'B': [10, 20, 30]
})
df2 = pd.DataFrame({
   'A': [1, 1, 1],
   'B': [2, 2, 2]
})
print("DataFrame 1：")
print(df1)
print("DataFrame 2：")
print(df2)
# 加法运算
print("加法运算：")
print(df1 + df2)
# 减法运算
print("减法运算：")
print(df1 - df2)
# 乘法运算
print("乘法运算：")
print(df1 * df2)
# 除法运算
# 结果为浮点数
print("除法运算：")
print(df1 / df2)
print(50 * "=")

# 2. 自动对齐机制
# 当两个 DataFrame 的行列索引不完全相同时，Pandas 会自动对齐，缺失值用 NaN 表示
df3 = pd.DataFrame({
   'A': [1, 2, 3],
   'B': [4, 5, 6]
}, index=['a', 'b', 'c'])
df4 = pd.DataFrame({
   'A': [10, 20],
   'C': [30, 40]
}, index=['b', 'c'])
print("DataFrame 3：")
print(df3)
print("DataFrame 4：")
print(df4)
print("自动对齐相加：")
# 只有 行索引 + 列名 完全一样的位置，才会计算数值
# 只要有一边找不到对应位置 → 结果 = NaN（空值）
print(df3 + df4)  # 行和列都会对齐
print(50 * "=")

# 3. 与标量运算
# 标量逐一和每一项进行计算
df = pd.DataFrame({
   'A': [1, 2, 3],
   'B': [4, 5, 6]
})
print("DataFrame：")
print(df)
# 与标量相加
print("加标量（10）：")
print(df + 10)
# 与标量相乘
print("乘标量（2）：")
print(df * 2)
# 其他运算
print("其他运算：")
print(df - 3)
print(df / 2)
print(df ** 2)
print(50 * "=")

# 4. 与 Series 运算（广播机制）
# DataFrame 与 Series 运算时，默认会将 Series 的索引与 DataFrame 的列对齐，按行进行广播
df = pd.DataFrame({
   'A': [1, 2, 3, 4],
   'B': [10, 20, 30, 40],
   'C': [100, 200, 300, 400]
})
s = pd.Series([1, 2, 3], index=['A', 'B', 'C'])
print("DataFrame：")
print(df)
print("Series：")
print(s)
# 按列对齐，按行广播
print("DataFrame - Series（按列广播）：")
print(df - s)
# 如果要按行运算，需要指定axis
print("按行运算（减去第一行）：")
print(df - df.iloc[0])
print(50 * "=")

# 5. 统计运算
# DataFrame 提供了丰富的统计函数，可以按行或按列进行计算
df = pd.DataFrame({
   'A': [1, 2, 3, 4],
   'B': [10, 20, 30, 40],
   'C': [100, 200, 300, 400]
})
print("DataFrame：")
print(df)
# 求和
# 默认操作列（axis=0）
print("求和：")
print("所有元素和：", df.sum().sum())
print("按列求和：", df.sum())  # 每列的和
print("按行求和：", df.sum(axis=1))  # 每行的和
# 平均值
print("平均值：")
print("按列平均值：", df.mean())
print("按行平均值：", df.mean(axis=1))
# 其他统计函数
print("其他统计：")
print("最大值：", df.max())
print("最小值：", df.min())
print("标准差：", df.std())
print("方差：", df.var())
print("中位数：", df.median())
print("描述性统计：")
print(df.describe())  # 生成综合统计信息
print(50 * "=")

# 4.5 Pandas DataFrame 的其他重要操作
# 1. 列操作（增删改）
df = pd.DataFrame({
   'A': [1, 2, 3],
   'B': [4, 5, 6]
})
print("原始DataFrame：")
print(df)
# 添加新列
# 添加方式类似字典
df['C'] = [7, 8, 9]
print("添加列C：")
print(df)
# 基于其他列计算新列
# 字典应该不可以这样添加，我印象中
df['D'] = df['A'] + df['B']
print("添加列D = A + B：")
print(df)
# 删除列
# del 经典删除
del df['D']
print("删除列D：")
print(df)
# 使用pop方法删除列（可以获取删除的值）
# pop（）, 指定列名精准删除
b_col = df.pop('B')
print("使用pop删除列B：")
print(df)
print("被删除的列B：")
print(b_col)
print(50 * "=")

# 2. 行操作（增删）
df = pd.DataFrame({
   'A': [1, 2, 3],
   'B': [4, 5, 6]
}, index=['a', 'b', 'c'])
print("原始DataFrame：")
print(df)
# 添加新行（使用loc）
df.loc['d'] = [7, 8]
print("添加行d：")
print(df)
# 删除行（使用drop）
df = df.drop('d')
print("删除行d：")
print(df)
# 删除多行
df = df.drop(['a', 'c'])
# 处逐一选择外，还可以切片删除
# 按位置序号切片删除：df.iloc[起始:结束].index
# 按标签索引切片删除：df.loc[起始标签:结束标签].index
print("删除行a和c：")
print(df)
print(50 * "=")

# 3. 数据对齐操作
df1 = pd.DataFrame({
   'A': [1, 2, 3],
   'B': [4, 5, 6]
}, index=['x', 'y', 'z'])
df2 = pd.DataFrame({
   'A': [10, 20],
   'C': [30, 40]
}, index=['y', 'z'])
print("df1：")
print(df1)
print("df2：")
print(df2)
# 使用align方法对齐
# 行列数相同，空位补NaN
# align() 是 pandas 用于将两个 DataFrame/Series 按索引和列对齐的核心方法
# 它会返回两个新对象，拥有完全相同的行索引和列名，方便后续加减乘除等运算
df1_aligned, df2_aligned = df1.align(df2)
print("对齐后：")
print("df1对齐后：")
print(df1_aligned)
print("df2对齐后：")
print(df2_aligned)
print(50 * "=")

# 4. 缺失值处理
df = pd.DataFrame({
   'A': [1, 2, None, 4],
   'B': [10, None, 30, 40],
   'C': [100, 200, 300, None]
})
print("包含缺失值的DataFrame：")
print(df)
# 检测缺失值
print("检测缺失值：")
print(df.isna())
print("缺失值统计：")
# 每列缺失值数量
print(df.isna().sum())
# 每行缺失值数量
print(df.isna().sum(axis=1))
# 删除含有缺失值的行
df_clean = df.dropna()
print("删除含有缺失值的行：")
print(df_clean)
# 删除含有缺失值的列
df_clean_col = df.dropna(axis=1)
print("删除含有缺失值的列：")
print(df_clean_col)
# 填充缺失值
df_filled = df.fillna(0)
print("用0填充缺失值：")
print(df_filled)
# 前向填充（用前一行的值填充）
df_ffill = df.fillna(method='ffill')
print("前向填充（ffill）：")
print(df_ffill)
# 后向填充（用后一行的值填充）
df_bfill = df.fillna(method='bfill')
print("后向填充（bfill）：")
print(df_bfill)
print(50 * "=")

# 5. 数据排序
df = pd.DataFrame({
   '姓名': ['张三', '李四', '王五', '赵六'],
   '年龄': [20, 22, 19, 21],
   '成绩': [85, 92, 78, 88]
})
print("原始DataFrame：")
print(df)
# 按年龄排序
df_sorted_age = df.sort_values('年龄')
print("按年龄升序排序：")
print(df_sorted_age)
# 按成绩降序排序
df_sorted_score = df.sort_values('成绩', ascending=False)
print("按成绩降序排序：")
print(df_sorted_score)
# 按多列排序（先按年龄升序，再按成绩降序）
df_multi_sorted = df.sort_values(['年龄', '成绩'], ascending=[True, False])
print("多列排序：")
print(df_multi_sorted)
# 按索引排序
df_sorted_index = df.sort_index()
print("按索引排序：")
print(df_sorted_index)
