import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.graphics.api import interaction_plot
import matplotlib.pyplot as plt


# 构造实验数据：燃料(A)、推进器(B)为两个影响因素，射程为目标变量
dic_t3 = [
    {'燃料': 'A1', '推进器': 'B1', '射程': 58.2}, {'燃料': 'A1', '推进器': 'B1', '射程': 52.6},
    {'燃料': 'A1', '推进器': 'B2', '射程': 56.2}, {'燃料': 'A1', '推进器': 'B2', '射程': 41.2},
    {'燃料': 'A1', '推进器': 'B3', '射程': 65.3}, {'燃料': 'A1', '推进器': 'B3', '射程': 60.8},
    {'燃料': 'A2', '推进器': 'B1', '射程': 49.1}, {'燃料': 'A2', '推进器': 'B1', '射程': 42.8},
    {'燃料': 'A2', '推进器': 'B2', '射程': 54.1}, {'燃料': 'A2', '推进器': 'B2', '射程': 50.5},
    {'燃料': 'A2', '推进器': 'B3', '射程': 51.6}, {'燃料': 'A2', '推进器': 'B3', '射程': 48.4},
    {'燃料': 'A3', '推进器': 'B1', '射程': 60.1}, {'燃料': 'A3', '推进器': 'B1', '射程': 58.3},
    {'燃料': 'A3', '推进器': 'B2', '射程': 70.9}, {'燃料': 'A3', '推进器': 'B2', '射程': 73.2},
    {'燃料': 'A3', '推进器': 'B3', '射程': 39.2}, {'燃料': 'A3', '推进器': 'B3', '射程': 40.7},
    {'燃料': 'A4', '推进器': 'B1', '射程': 75.8}, {'燃料': 'A4', '推进器': 'B1', '射程': 71.5},
    {'燃料': 'A4', '推进器': 'B2', '射程': 58.2}, {'燃料': 'A4', '推进器': 'B2', '射程': 51.0},
    {'燃料': 'A4', '推进器': 'B3', '射程': 48.7}, {'燃料': 'A4', '推进器': 'B3', '射程': 41.4},
]
df = pd.DataFrame(dic_t3)

# 构建有交互作用的双因素方差分析模型
formula = '射程 ~ C(燃料) + C(推进器) + C(燃料):C(推进器)'
model = ols(formula, data=df).fit()

# 输出方差分析结果
anova_result = anova_lm(model, typ=1)
print(anova_result)

# 交互效应可视化，分析因素组合的影响
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig = interaction_plot(
    x=df['燃料'], trace=df['推进器'], response=df['射程'],
    ylabel='射程', xlabel='燃料类型'
)
plt.title('燃料×推进器交互效应图')
plt.show()

# 事后检验：Tukey HSD 分析因素水平间的显著差异
from statsmodels.stats.multicomp import pairwise_tukeyhsd
print(pairwise_tukeyhsd(df['射程'], df['燃料'], alpha=0.01))