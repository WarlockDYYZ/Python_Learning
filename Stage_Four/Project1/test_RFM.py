import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import plotly.express as px
import streamlit as st


# 创建模拟用户行为数据
np.random.seed(42)
user_ids = np.random.randint(1, 10001, size=30000)
purchase_dates = [datetime.now() - timedelta(days=np.random.randint(1, 365)) for _ in range(30000)]
purchase_amounts = np.random.normal(loc=200, scale=100, size=30000)
purchase_amounts[purchase_amounts < 0] = 0  # 避免负金额

df = pd.DataFrame({
    'user_id': user_ids,
    'purchase_date': purchase_dates,
    'purchase_amount': purchase_amounts
})

# 设定分析基准日期（通常为数据最新日期的次日）
analysis_date = df['purchase_date'].max() + timedelta(days=1)

# 计算RFM指标
rfm = df.groupby('user_id').agg({
    'purchase_date': lambda x: (analysis_date - x.max()).days,  # R值：最近消费天数
    'purchase_date': 'count',  # F值：消费频次
    'purchase_amount': 'sum'  # M值：消费金额
}).reset_index()

# 重命名列
rfm.columns = ['user_id', 'R', 'F', 'M']


# 使用分位数进行分箱并评分（5分制）
for metric in ['R', 'F', 'M']:
    rfm[f'{metric}_score'] = pd.qcut(rfm[metric], q=5, labels=False, duplicates='drop')

# R值越小表示越活跃，因此需要反向评分
rfm['R_score'] = rfm['R_score'].apply(lambda x: 5 - x if x != 0 else 0)

# F和M值越大表示越活跃，保持正向评分
rfm['F_score'] = rfm['F_score'].apply(lambda x: x + 1)
rfm['M_score'] = rfm['M_score'].apply(lambda x: x + 1)


# 计算RFM总分
rfm['RFM_total'] = rfm['R_score'] + rfm['F_score'] + rfm['M_score']

# 基于总分划分用户群
rfm['user_segment'] = '低价值用户'
rfm.loc[rfm['RFM_total'] >= 12, 'user_segment'] = '高价值用户'
rfm.loc[(rfm['RFM_total'] >= 9) & (rfm['RFM_total'] < 12), 'user_segment'] = '中价值用户'

# 或更细粒度的分群
rfm['detailed_segment'] = '低价值沉睡用户'
rfm.loc[(rfm['R_score'] >= 4) & (rfm['F_score'] >= 4) & (rfm['M_score'] >= 4), 'detailed_segment'] = '高价值忠诚客户'
rfm.loc[(rfm['R_score'] >= 4) & (rfm['F_score'] < 4) & (rfm['M_score'] < 4), 'detailed_segment'] = '新激活客户'
rfm.loc[(rfm['R_score'] < 4) & (rfm['F_score'] < 4) & (rfm['M_score'] < 4), 'detailed_segment'] = '沉默用户'


# 标准化RFM指标
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm[['R', 'F', 'M']])

# 使用肘部法则选择最佳簇数
sse = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(rfm_scaled)
    sse.append(kmeans.inertia_)

# 绘制SSE曲线
fig = px.line(x=range(1, 11), y=sse, title='肘部法则选择最佳簇数')
st.plotly_chart(fig)

# 拟合K-means模型（假设选择4个簇）
kmeans = KMeans(n_clusters=4, random_state=42)
kmeans.fit(rfm_scaled)

# 添加聚类标签
rfm['cluster_label'] = kmeans.labels_

# 分析聚类中心
cluster_Centers = pd.DataFrame(kmeans.cluster_centers_, columns=['R', 'F', 'M'])

# 可视化聚类结果
fig = px.scatter(rfm, x='F', y='M', color='cluster_label', title='RFM聚类可视化（F vs M）')
st.plotly_chart(fig)


from sklearn.semi_supervised import LabelPropagation
from sklearn.metrics.pairwise import cosine_similarity

# 构建用户行为相似性矩阵
user_behavior_matrix = df.pivot_table(index='user_id', columns='event_type', values='count', aggfunc='sum').fillna(0)

# 计算余弦相似度矩阵
similarity_matrix = cosine_similarity(user_behavior_matrix)

# 初始化标签传播模型
lp = LabelPropagation(gamma=20, max_iter=1000)
lp.fit(similarity_matrix)

# 获取标签
cluster_labels = lp.labels_

# 添加标签到用户数据
user_behavior_matrix['cluster_label'] = cluster_labels