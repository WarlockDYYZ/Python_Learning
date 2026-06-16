import pandas as pd
import numpy as np


df = pd.read_csv("Ecommerce_Sales_Data.csv", parse_dates=['Order Date'])


# 数据清洗：处理缺失值、异常值、重复值
df = df.dropna(subset=['Customer Name', 'Order ID'])  # 剔除核心缺失值的无效订单
df = df[df['Quantity'] > 0]  # 剔除退货、赠品等无效交易数据
df = df[df['Unit Price'] > 0]  # 剔除无效定价的商品数据
df = df.drop_duplicates(subset=['Order ID', 'Product Name', 'Quantity'])  # 剔除完全重复的无效订单

# 新增辅助分析字段：交易金额、交易日期维度
df['Sales'] = df['Quantity'] * df['Unit Price']
df['InvoiceYearMonth'] = df['Order Date'].dt.to_period('M')

# 数据过滤：剔除异常交易数据
df = df[(df['Sales'] < df['Sales'].quantile(0.99)) & (df['Sales'] > 0)]

print(df.head())