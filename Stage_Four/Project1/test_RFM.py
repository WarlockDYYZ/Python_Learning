import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go


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


# 引入轮廓系数评估指标
from sklearn.metrics import silhouette_score

# 1. Log变换处理极端值（在标准化前进行，应对长尾分布）
rfm_log = np.log1p(rfm[['R', 'F', 'M']])

# 2. 标准化RFM指标（对Log变换后的数据进行标准化）
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm_log)

# 3. 使用肘部法则结合轮廓系数选择最佳簇数
sse = []
sil_scores = []
for k in range(2, 11):  # 轮廓系数要求K>=2，因此从2开始
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(rfm_scaled)
    sse.append(kmeans.inertia_)
    # 计算并记录轮廓系数
    sil_scores.append(silhouette_score(rfm_scaled, kmeans.labels_))

# 4. 绘制SSE与轮廓系数双重验证曲线（双Y轴）
fig = go.Figure()

# 左 Y 轴：SSE 曲线（寻找拐点）
fig.add_trace(go.Scatter(x=list(range(2, 11)), y=sse, name='SSE (肘部法则)',
 line=dict(color='royalblue', width=2)))

# 右 Y 轴：轮廓系数曲线（寻找最高点）
fig.add_trace(go.Scatter(x=list(range(2, 11)), y=sil_scores, name='轮廓系数',
 line=dict(color='crimson', width=2), yaxis='y2'))

# 配置双 Y 轴布局
fig.update_layout(
    title='K值寻优：双重验证',
    xaxis_title='簇数 (K)',
    yaxis_title='SSE',
    yaxis2=dict(title='轮廓系数', overlaying='y', side='right'),
    template='plotly_white'
)
st.plotly_chart(fig)

# 5. 拟合K-means模型（假设选择4个簇）
kmeans = KMeans(n_clusters=4, random_state=42)
kmeans.fit(rfm_scaled)

# 6. 添加聚类标签
rfm['cluster_label'] = kmeans.labels_

# 7. 分析聚类中心（注意：此时中心点为Log变换并标准化后的值）
cluster_centers = pd.DataFrame(kmeans.cluster_centers_, columns=['R', 'F', 'M'])

# 8. 可视化聚类结果
fig = px.scatter(rfm, x='F', y='M', color='cluster_label', title='RFM聚类可视化（F vs M）')
st.plotly_chart(fig)


from sklearn.semi_supervised import LabelPropagation
from sklearn.metrics.pairwise import cosine_similarity

# 1. 构建用户行为矩阵
user_behavior_matrix = df.pivot_table(
    index='user_id', columns='event_type', values='count', aggfunc='sum'
).fillna(0)

# 2. 计算余弦相似度矩阵
similarity_matrix = cosine_similarity(user_behavior_matrix)

# 3. 【关键补充】构造初始标签 (y)
# 假设我们有 1000 个用户，其中前 10 个是已知的高价值用户(标签1)，
# 第 11-20 个是已知的流失用户(标签2)，其余 980 个用户标签设为 -1（代表未知，等待算法预测）
y = np.full(len(user_behavior_matrix), -1)
y[:10] = 1   # 种子标签：高价值用户
y[10:20] = 2 # 种子标签：流失用户

# 4. 初始化并拟合标签传播模型（传入相似度矩阵和初始标签）
lp = LabelPropagation(max_iter=1000)
lp.fit(similarity_matrix, y=y)

# 5. 获取预测标签并拼接
cluster_labels = lp.labels_
user_behavior_matrix['cluster_label'] = cluster_labels