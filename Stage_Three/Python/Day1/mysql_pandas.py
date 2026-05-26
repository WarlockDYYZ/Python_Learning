import pandas as pd
import pymysql
from sqlalchemy import create_engine


# 创建数据库连接引擎
engine = create_engine("mysql+pymysql://root:123456@localhost:3306/data_analysis")

# 从数据库读取数据到DataFrame
df = pd.read_sql("SELECT * FROM income_data", engine)
print("数据读取成功，共有%d条记录" % len(df))
# 显示前5条记录
print("n数据预览：")
print(df.head())


# 构造 1 条数据（字典 → DataFrame）
data = {
    "name": ["小明"],
    "department": ["运营部"],
    "salary": [6500.00],
    "bonus": [1000.00],
    "work_years": [2],
    "create_time": ["2025-12-26"]
}
# 转换成 DataFrame 对象
df = pd.DataFrame(data)

# 使用 to_sql 插入 1 条数据
df.to_sql(
    name="income_data",      # 表名
    con=engine,              # 连接
    if_exists="append",      # 追加数据
    index=False              # 不插入索引列
)
print("插入一条数据")

# 查询最后一条数据
df_check = pd.read_sql("SELECT * FROM income_data ORDER BY id DESC LIMIT 1", engine)
print("刚插入的数据：")
print(df_check)