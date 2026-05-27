import pandas as pd
from sqlalchemy import create_engine


def process_data(chunk):
    print(chunk)


# 创建数据库连接引擎
engine = create_engine("mysql+pymysql://root:123456@localhost:3306/data_analysis")

# 分批读取大表数据（每次读取1000条）
chunk_size = 1000
total_count = 0
for chunk in pd.read_sql("SELECT * FROM income_data", engine, chunksize=chunk_size):
    # 处理每批数据
    process_data(chunk)

    total_count += len(chunk)
    print(f"已处理{total_count}条记录")
print(f"n共处理{total_count}条记录")