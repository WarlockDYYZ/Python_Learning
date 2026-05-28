import pymysql


# MySQL 配置与测试
db_config = {
    "host": "127.0.0.1",      # 数据库主机地址
    "port": 3306,             # MySQL默认端口
    "user": "root",           # 用户名
    "password": "123456", # 密码
    "database": "data_analysis",    # 数据库名
    "charset": "utf8mb4"      # 字符集，推荐使用utf8mb4支持emoji
}

# MySQL 连接
conn = pymysql.connect(**db_config)
cursor = conn.cursor()

# 销售数据分析
sales_analysis_sql = """
SELECT
    t.region,
    p.category,
    SUM(s.quantity) AS total_quantity,
    SUM(s.quantity * s.price) AS total_revenue,
    AVG(s.price) AS avg_price,
    MAX(s.price) AS max_price,
    MIN(s.price) AS min_price
FROM sales_data AS s
JOIN products AS p
    ON s.product_id = p.product_id
JOIN territories AS t
    ON s.territory_id = t.territory_id
WHERE s.sale_date >= %s AND s.sale_date < %s
GROUP BY t.region, p.category
HAVING total_quantity > 100
ORDER BY total_revenue DESC;
"""
# 执行查询（2023年全年数据）
cursor.execute(sales_analysis_sql, ("2023-01-01", "2024-01-01"))
results = cursor.fetchall()


# 转换为DataFrame进行进一步分析
import pandas as pd


columns = ["region", "category", "total_quantity", "total_revenue", "avg_price", "max_price", "min_price"]
df = pd.DataFrame(results, columns=columns)  # 必须加 columns
print("\n销售数据分析结果：")
print(df.to_string(index=False))


# 使用pandas进行可视化
import matplotlib.pyplot as plt


plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
# 绘制各地区销售总额对比
plt.figure(figsize=(12, 8))

# 把 revenue 转成数字类型（关键修复）
df["total_revenue"] = pd.to_numeric(df["total_revenue"])
df["total_quantity"] = pd.to_numeric(df["total_quantity"])
region_revenue = df.groupby('region')['total_revenue'].sum()
region_revenue.plot(kind='bar', color='skyblue')

plt.title('Sales Revenue by Region (2023)', fontsize=14, fontweight='bold')
plt.xlabel('Region')
plt.ylabel('Revenue (USD)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()