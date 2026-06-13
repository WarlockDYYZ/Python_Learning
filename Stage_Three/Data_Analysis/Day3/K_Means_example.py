import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA


# 1. 模拟电商用户数据（复现真实用户行为分布）
np.random.seed(42)
n_users = 500
data = {
    'user_id': range(1, n_users+1),
    # Recency：最近购买距今天数（指数分布，模拟用户流失分布）
    'recency_days': np.random.exponential(scale=30, size=n_users).astype(int) + 1,
    # Frequency：过去90天购买次数（负二项分布，模拟高频用户长尾分布）
    'purchase_count': np.random.negative_binomial(n=2, p=0.3, size=n_users) + 1,
    # Monetary：累计消费金额（对数正态分布，模拟消费金额长尾分布）
    'total_spend': np.random.lognormal(mean=6, sigma=1.5, size=n_users).round(2),
    'avg_order_value': np.random.lognormal(mean=5, sigma=1.2, size=n_users).round(2),
    'favorites_count': np.random.poisson(lam=8, size=n_users),
    'coupon_used': np.random.binomial(n=1, p=0.6, size=n_users)
}
df = pd.DataFrame(data)
print(df.head())

# 2. 特征选择与标准化
# 剔除user_id与coupon_used，选择核心行为/消费特征
features = ['recency_days', 'purchase_count', 'total_spend', 'avg_order_value', 'favorites_count']
X = df[features].copy()

# 标准化：K-Means基于距离计算，必须消除量纲差异
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# 3. 肘部法则+轮廓系数选择最优K值
k_range = range(2, 11)
sse_list = []  # 簇内误差平方和，衡量聚类同质化
silhouette_list = []  # 轮廓系数，衡量聚类相似度与区分度

for k in k_range:
    # 使用K-Means++初始化，提升聚类稳定性
    kmeans = KMeans(n_clusters=k, n_init=20, max_iter=500, random_state=42)
    kmeans.fit(X_scaled)
    # 记录SSE与轮廓系数
    sse_list.append(kmeans.inertia_)
    silhouette_list.append(silhouette_score(X_scaled, kmeans.labels_))

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 可视化对比，选择最优K值
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
# 肘部法则图：定位SSE下降拐点
ax1.plot(k_range, sse_list, 'bo-', linewidth=2, markersize=8)
ax1.set_xlabel('K值（聚类数量）', fontsize=12)
ax1.set_ylabel('簇内误差平方和（SSE）', fontsize=12)
ax1.set_title('肘部法则：确定最优K值', fontsize=14)
ax1.axvline(x=4, color='red', linestyle='--', alpha=0.7, label='建议K=4')
ax1.legend()

# 轮廓系数图：定位得分最高点
ax2.bar(k_range, silhouette_list, color='steelblue', alpha=0.8)
ax2.set_xlabel('K值（聚类数量）', fontsize=12)
ax2.set_ylabel('轮廓系数', fontsize=12)
ax2.set_title('轮廓系数：越高越好', fontsize=14)
best_k = k_range[silhouette_list.index(max(silhouette_list))]
ax2.bar(best_k, max(silhouette_list), color='red', alpha=0.8, label=f'最优K={best_k}')
ax2.legend()
plt.tight_layout()
plt.show()


# 4. 训练最终模型（根据上图选择最优K值）
K_FINAL = 4
kmeans_final = KMeans(n_clusters=K_FINAL, n_init=20, max_iter=500, random_state=42)
cluster_labels = kmeans_final.fit_predict(X_scaled)

# 将聚类标签合并到原始数据
df['cluster'] = cluster_labels

# 5. 聚类结果分析：构建用户画像
cluster_profile = df.groupby('cluster')[features].mean().round(2)
print("各簇用户特征均值：")
print(cluster_profile)

# 计算各群组占比，辅助运营优先级判断
cluster_counts = df['cluster'].value_counts().sort_index()
print("\n各簇用户数量占比：")
for cluster_id, count in cluster_counts.items():
    print(f"簇{cluster_id}: {count}人（{count/len(df)*100:.1f}%）")

# 6. 可视化：PCA降维后展示聚类分布
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_scaled)
plt.figure(figsize=(10, 6))
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=cluster_labels, palette='deep', alpha=0.7)
plt.title('电商用户聚类分布（PCA降维）', fontsize=14)
plt.legend(title='用户群组')
plt.tight_layout()
plt.show()