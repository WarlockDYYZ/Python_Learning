import pandas as pd
import warnings

# 屏蔽样式警告（可选）
warnings.filterwarnings('ignore')

# 1. 读取 Excel 文件
df = pd.read_excel(r'C:\Users\Administrator\Desktop\(T-1日)下载明细：进线咨询明细.xlsx', engine='openpyxl')

# 根据列名填充
# 值为空的单元格认为是0，填充0
column_name = "是否升级（1是 0 否）"
df[column_name] = df[column_name].fillna(0)

# 利用 Pandas 的链式调用，将原本杂乱的流水账数据，一步到位地转换成了清晰的交叉统计表
# 先分组 -> 再计数 -> 最后把结果“转”成宽表
# 1. df.groupby('坐席姓名') —— 【分组】
# 动作：把整个表格按照“坐席姓名”这一列进行归类，相同名字为一组
# 2. ['是否升级（1是 0 否）'] —— 【选列】
# 动作：在分好组的每一堆里，只盯着“是否升级”这一列看
# 3. .value_counts() —— 【计数】
# 动作：统计每一组里，0 和 1 分别出现了多少次
# (注意：此时 0 和 1 还是挤在同一列里的)
# 4. .unstack(fill_value=0) —— 【透视/展开】
# 动作：unstack 的作用是把最内层的索引（也就是刚才统计出来的 0 和 1）“提”出来变成列名
# fill_value=0 就是告诉 Pandas：“如果有空缺的地方，直接填 0，不要填 NaN”，默认没有对应列时填NaN
result = df.groupby('坐席姓名')['是否升级（1是 0 否）'].value_counts().unstack(fill_value=0)
result.columns = ['未升级次数(0)', '升级次数(1)']
print(result) # <class 'pandas.DataFrame'>

# 1. 强制转换列的数据类型为数字
# errors='coerce' 的意思是：如果遇到无法转换的内容（比如 "abc"），就把它变成空值 (NaN)，防止报错
result['未升级次数(0)'] = pd.to_numeric(result['未升级次数(0)'], errors='coerce')
result['升级次数(1)'] = pd.to_numeric(result['升级次数(1)'], errors='coerce')

# 2. (可选) 填充空值
# 如果转换过程中产生了 NaN，计算结果也会是 NaN。如果希望它们算作 0，可以加上这一行：
result = result.fillna(0)

# 3. 再次检查类型（确认变为 float64 或 int64）
print(result.dtypes)

# 4. 现在可以安全地进行除法计算了
result['升级率'] = result['升级次数(1)'] / (result['未升级次数(0)'] + result['升级次数(1)'])
print(result.head())

# 3. 保存文件
# 默认 index=True，即写入行索引
result.to_excel(r'C:\Users\Administrator\Desktop\upgrade_rate.xlsx', engine='openpyxl')

print(f"成功处理，已保存")