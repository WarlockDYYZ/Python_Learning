import pandas as pd
import numpy as np


# 创建一个带有自定义行索引的 DataFrame
data = {
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9]
}
df = pd.DataFrame(data, index=['row1', 'row2', 'row3'])

# 1. 使用 .at 访问单个值（获取 row2 行 B 列的值）
value = df.at['row2', 'B']
print("访问到的值:", value)  # 输出: 5

# 2. 使用 .at 修改单个值（将 row1 行 A 列的值改为 10）
df.at['row1', 'A'] = 10
print("\n修改后的 DataFrame:\n", df)
print('*' * 100)


# 创建普通 DataFrame
df2 = pd.DataFrame({
    "姓名": ["张三", "李四", "王五"],
    "年龄": [25, 30, 28],
    "城市": ["北京", "上海", "深圳"]
})

# 使用 .at 访问第 1 行（索引为1）的“姓名”列
name = df2.at[1, "姓名"]
print("姓名:", name)  # 输出: 李四
# 注意：如果需要通过绝对位置（如第1行第1列）访问，应使用 .iat[0, 0]

# 多种方式创建多级索引
# 方法一：从元组列表创建 (from_tuples)
arrays = [['电子产品', '电子产品', '家居用品', '家居用品'],
          ['手机', '电脑', '沙发', '灯具']]
tuples = list(zip(*arrays))
multi_index = pd.MultiIndex.from_tuples(tuples, names=['大类', '小类'])
df_multi = pd.DataFrame(np.random.randint(10, 100, size=(4, 2)),
                        index=multi_index,
                        columns=['销量', '销售额'])

# 方法二：从已有 DataFrame 直接创建 (set_index)
df_flat = pd.DataFrame({
    '大区': ['华北', '华北', '华东', '华东'],
    '省份': ['北京', '天津', '上海', '江苏'],
    '营收': [100, 80, 120, 150]
})
df_hier = df_flat.set_index(['大区', '省份'])


# 多级索引的数据选择与操作
# 1. 选择第一级索引为 '电子产品' 的所有数据
print(df_multi.loc['电子产品'])
# 2. 精确选择特定组合（大类='电子产品', 小类='手机'）
print(df_multi.loc[('电子产品', '手机')])
# 3. 跨层级选取数据（使用 xs 方法截取指定级别）
# 选取所有“小类”为“手机”的数据，无论它属于哪个大类
print(df_multi.xs('手机', level='小类'))
# 4. 在多级索引上进行分组聚合
# 计算每个“大类”的平均销量
grouped_mean = df_multi.groupby(level='大类')['销量'].mean()
print(grouped_mean)
print('*' * 100)


# 基础数据处理
# 处理缺失值
df['折扣'] = [0.8, None, 0.9]
df['销量'] = [100, 200, 300]
df['产品'] = ['Phone', 'Computer', 'Car']
print("\n修改前的 DataFrame:\n", df)

df['折扣'].fillna(1.0, inplace=True)  # 填充缺失值
df.dropna(subset=['销量'], inplace=True)  # 删除特定列的缺失值
# 字符串处理
df['产品描述'] = df['产品'].str.upper() + ' - 高端产品'  # 字符串操作
# 时间序列处理
df['日期'] = pd.to_datetime(['2026-01-15', '2026-02-20', '2026-03-10'])
df['月份'] = df['日期'].dt.month  # 提取月份
print("\n修改后的 DataFrame:\n", df)