import pandas as pd
import warnings

# 屏蔽样式警告（可选）
warnings.filterwarnings('ignore')

# 读取 Excel 文件
df = pd.read_excel(r'C:\Users\Administrator\Desktop\进线咨询明细.xlsx', engine='openpyxl')

# 根据列名填充，值为空的单元格认为是0，填充0
column_name = "是否升级（1是 0 否）"
df[column_name] = df[column_name].fillna(0)

result = df.groupby('坐席姓名')['是否升级（1是 0 否）'].value_counts().unstack(fill_value=0)
result.columns = ['未升级次数(0)', '升级次数(1)']

print(df.groupby('坐席姓名'))
'''
    返回 DataFrameGroupBy 对象
    一个“待命”的中间状态或者是一个分组迭代器。
    它只是把数据按照的要求划分好了组，但还没有进行任何实际的计算或提取操作，所以直接 print 只能看到它的内存地址信息，看不到具体的数据内容。
'''
print(df.groupby('坐席姓名')['是否升级（1是 0 否）'])
'''
    返回 SeriesGroupBy 对象
    指向特定列数据的分组迭代器。
    把数据按‘坐席姓名’分组，只关心每组里的‘是否升级（1是 0 否）’这一列”。
    但它还没有进行任何实际的计算或提取，所以直接打印只能看到它的内存地址信息。
'''
print(df.groupby('坐席姓名')['是否升级（1是 0 否）'].value_counts())
'''
    print(result['张三'])
    是否升级（1是 0 否）
    0    5
    1    3
    Name: count, dtype: int64
    多层索引（MultiIndex）的强大之处。你可以把它想象成一个嵌套的字典结构：
    第一层键是“坐席姓名”（比如 '张三'）。
    第二层键是“是否升级的状态”（比如 0 或 1）。
    print(result['张三'][0])  # 输出: 5
    返回值是一个带有多层索引（MultiIndex）的 Pandas Series 对象
    左边的 坐席姓名 和 是否升级（1是 0 否） 这两列，共同组成了这个 Series 的索引（Index）。
    视觉效果上会隐藏下面的姓名，但在内存中信息是完整的
'''
print(df.groupby('坐席姓名')['是否升级（1是 0 否）'].value_counts().unstack())
'''
    展开成宽表（让 0 和 1 变成列名）
    使用 .unstack() 方法，把第二层索引（0 和 1）“提起来”变成真正的列名，这样看起来就像一张交叉统计表。
    fill_value=0 ：“如果有空缺的地方，直接填 0，不要填 NaN”，默认没有对应列时填NaN
'''
print(result) # <class 'pandas.DataFrame'>

# 强制转换列的数据类型为数字
# errors='coerce' ：如果遇到无法转换的内容（比如 "abc"），就把它变成空值 (NaN)，防止报错
result['未升级次数(0)'] = pd.to_numeric(result['未升级次数(0)'], errors='coerce')
result['升级次数(1)'] = pd.to_numeric(result['升级次数(1)'], errors='coerce')


# 如果转换过程中产生了 NaN，计算结果也会是 NaN。将它们算作 0
result = result.fillna(0)

# 再次检查类型（确认变为 float64 或 int64）
print(result.dtypes)

# 计算升级率
result['升级率'] = result['升级次数(1)'] / (result['未升级次数(0)'] + result['升级次数(1)'])
print(result.head())

# 保存文件
# 默认 index=True，即写入行索引
result.to_excel(r'C:\Users\Administrator\Desktop\upgrade_rate.xlsx', engine='openpyxl')

print(f"成功处理，已保存")
'''
print("按下回车键退出程序...")
input()
print("程序已退出")
'''
