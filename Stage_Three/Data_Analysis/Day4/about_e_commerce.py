import pandas as pd
import numpy as np


# 数据集的加载与清洗代码参考
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
print(df.head().to_string())


# 构建RFM模型特征
# 统计截止时间设置为数据集中最近订单的后一天
latest_date = df['Order Date'].max() + pd.Timedelta(days=1)
rfm = df.groupby('Customer Name').agg(
    Recency=('Order Date', lambda x: (latest_date - x.max()).days),
    Frequency=('Order ID', 'nunique'),
    Monetary=('Sales', 'sum')
).reset_index()

# 对RFM特征进行标准化处理：适配K-Means的距离计算要求
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])
print('\n\n' + str(rfm_scaled))


# 用肘部法则确定最优聚类数量
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt


plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

sse = []
silhouette_scores = []
k_range = range(2, 10)
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=20)
    kmeans.fit(rfm_scaled)
    sse.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(rfm_scaled, kmeans.labels_))

# 可视化：绘制肘部法则图与轮廓系数图，综合选择最优K值
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
ax1.plot(k_range, sse, 'bo-', linewidth=2)
ax1.set_xlabel('聚类数量K')
ax1.set_ylabel('簇内误差平方和（SSE）')
ax1.set_title('肘部法则：选择最优K值')
ax1.axvline(x=4, color='red', linestyle='--', alpha=0.7)

ax2.plot(k_range, silhouette_scores, 'go-', linewidth=2)
ax2.set_xlabel('聚类数量K')
ax2.set_ylabel('轮廓系数')
ax2.set_title('轮廓系数：越高越好')
ax2.axvline(x=4, color='red', linestyle='--', alpha=0.7)
plt.show()


# 训练最终K-Means模型，为用户打上价值群组标签
kmeans_final = KMeans(n_clusters=4, random_state=42, n_init=20)
rfm['Cluster'] = kmeans_final.fit_predict(rfm_scaled)

# 分析每个群组的RFM特征均值，总结群组特征
cluster_profile = rfm.groupby('Cluster').agg(
    最近购买天数=('Recency', 'mean'),
    消费频率=('Frequency', 'mean'),
    消费金额=('Monetary', 'mean'),
    用户数量=('Customer Name', 'count')
).round(2)
print(cluster_profile.to_string())

# 计算各群组用户数量占比，辅助运营优先级决策
cluster_percent = rfm['Cluster'].value_counts(normalize=True).round(4) * 100
print(cluster_percent.to_string())


# PCA降维到2维，便于在平面上可视化聚类分布
from sklearn.decomposition import PCA


pca = PCA(n_components=2, random_state=42)
rfm_pca = pca.fit_transform(rfm_scaled)

# 定义群组配色和业务标签，确保可视化配色与业务含义绑定
cluster_colors = ['#2ecc71', '#3498db', '#f1c40f', '#e74c3c']
cluster_labels = ['高价值活跃用户', '成长潜力用户', '普通新用户', '沉睡流失风险用户']

# 绘制散点图，直观展示用户群组分布效果
plt.figure(figsize=(10, 6))
for i in range(4):
    plt.scatter(
        rfm_pca[rfm['Cluster'] == i, 0],
        rfm_pca[rfm['Cluster'] == i, 1],
        c=cluster_colors[i],
        label=cluster_labels[i],
        alpha=0.7, s=50
    )
plt.xlabel('PCA维度1')
plt.ylabel('PCA维度2')
plt.title('电商用户价值聚类分布（PCA降维）', fontsize=14)
plt.legend(title='用户群组')
plt.show()


# 构建回归分析数据集：按交易月度聚合
reg_data = df.groupby(['InvoiceYearMonth', 'CustomerID', 'TVAdSpend', 'RadioAdSpend', 'NewspaperAdSpend']).agg(
    Revenue=('Sales', 'sum')
).reset_index()

# 匹配用户聚类标签，将用户群组特征引入回归模型，分析不同群组的价值贡献
reg_data = reg_data.merge(rfm[['CustomerID', 'Cluster']], on='CustomerID', how='left')

# 定义回归模型的公式，引入交互项，分析渠道组合的协同效果
import statsmodels.formula.api as smf
# 公式中C(Cluster)将群组作为分类变量处理，TVAdSpend:RadioAdSpend表示两者的交互项
formula = 'Revenue ~ TVAdSpend + RadioAdSpend + NewspaperAdSpend + C(Cluster) + TVAdSpend:RadioAdSpend'