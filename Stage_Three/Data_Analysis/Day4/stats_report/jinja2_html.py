import base64
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Template


plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 定义符合公司规范的HTML报告模板
template_str = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>商业分析报告</title>
    <style>
        body { font-family: "Microsoft Yahei", sans-serif; margin: 30px; }
        .section { margin-bottom: 30px; }
        .title { font-size: 24px; font-weight: bold; color: #2c3e50; }
        .subtitle { font-size: 18px; font-weight: bold; color: #34495e; margin: 10px 0; }
        .content { font-size: 14px; line-height: 1.6; color: #333; }
        .chart { margin: 15px 0; text-align: center; }
        .table { width: 100%; border-collapse: collapse; margin: 15px 0; }
        .table th, .table td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        .table th { background-color: #f5f5f5; }
    </style>
</head>
<body>
    <!-- 执行摘要 -->
    <div class="section">
        <div class="title">核心摘要</div>
        <div class="content">{{ executive_summary }}</div>
    </div>

    <!-- 回归分析结论 -->
    <div class="section">
        <div class="title">一、驱动因素分析</div>
        <div class="subtitle">1.1 核心影响因素</div>
        <div class="content">{{ regression_conclusion }}</div>
        <div class="chart">
            <img src="data:image/png;base64,{{ regression_chart }}" alt="回归分析图表">
            <div class="chart-desc">数据来源：{{ data_source }}，统计时间：{{ stat_date }}</div>
        </div>
    </div>

    <!-- 聚类分析结论 -->
    <div class="section">
        <div class="title">二、用户细分洞察</div>
        <div class="subtitle">2.1 用户群体分层</div>
        <div class="content">{{ clustering_conclusion }}</div>
        <div class="chart">
            <img src="data:image/png;base64,{{ clustering_chart }}" alt="聚类分析图表">
            <div class="chart-desc">数据来源：{{ data_source }}，统计时间：{{ stat_date }}</div>
        </div>
    </div>

    <!-- 业务建议 -->
    <div class="section">
        <div class="title">三、战略建议</div>
        <div class="content">{{ recommendations }}</div>
    </div>
</body>
</html>
"""

# 2. 定义将Matplotlib图表转为Base64字符串的辅助函数
def plt_to_base64(fig):
    """将Matplotlib图表转换为Base64编码，直接嵌入HTML报告"""
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

# 3. 模拟分析结果（实际场景中从建模代码中获取）
executive_summary = "基于过去90天的用户行为与交易数据，TV广告和高价值用户群体是影响销售额的两大核心关键因素；其中，TV广告的投入产出比最优，而高价值用户群体的复购率直接决定了销售额的基础盘。"
regression_conclusion = "TV广告的投入产出比最优，边际效益显著；报纸广告的投入对销售额没有显著独立影响。"
clustering_conclusion = "我们将用户分为4个特征显著的群体，其中“高价值活跃用户”贡献了近80%的利润，“沉睡流失风险用户”的流失概率显著高于其他群体。"
recommendations = "建议将报纸广告的预算，优先转移到TV广告的黄金时段投放；将运营资源重点投向高价值活跃用户的专属权益体系，同时针对沉睡用户群体，设计专属召回方案，优先提升该群体的活跃度。"
data_source = "公司内部交易系统、用户行为埋点数据"
stat_date = "2026年1月-3月"

# 4. 生成模拟回归分析图表
fig_reg, ax = plt.subplots(figsize=(8, 5))
ax.bar(['TV广告', '社交媒体', '报纸广告'], [0.045, 0.028, 0.002], color=['#2ecc71', '#3498db', '#e74c3c'])
ax.set_title('各广告渠道边际效益对比', fontsize=14)
ax.set_ylabel('边际效益（销售额/元）', fontsize=12)
regression_chart = plt_to_base64(fig_reg)

# 5. 生成模拟聚类分析图表
fig_clust, ax = plt.subplots(figsize=(8, 5))
ax.scatter([1,2,3,4], [2,4,6,8], c=['#2ecc71', '#3498db', '#f1c40f', '#e74c3c'], s=100)
ax.set_title('用户群体特征分布', fontsize=14)
ax.set_xlabel('最近购买时间', fontsize=12)
ax.set_ylabel('累计消费金额', fontsize=12)
clustering_chart = plt_to_base64(fig_clust)

# 6. 渲染并保存HTML报告
template = Template(template_str)
html_out = template.render(
    executive_summary=executive_summary,
    regression_conclusion=regression_conclusion,
    clustering_conclusion=clustering_conclusion,
    recommendations=recommendations,
    regression_chart=regression_chart,
    clustering_chart=clustering_chart,
    data_source=data_source,
    stat_date=stat_date
)

with open("商业级分析报告.html", "w", encoding="utf-8") as f:
    f.write(html_out)