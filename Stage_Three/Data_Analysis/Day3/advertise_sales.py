import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# 加载数据集（在线加载失败则使用模拟数据）
# 仅提取 2~5 列，对应 TV（电视）、Radio（广播）、Newspaper（报纸）的广告花费以及对应的 Sales（销售额）
df = pd.read_csv('Advertising.csv', usecols=[1,2,3,4])

# 一元线性回归：单独分析TV广告的影响
model_tv = smf.ols(formula='Sales ~ TV', data=df).fit()
print("=== 一元回归（TV）摘要 ===")
print(model_tv.summary())

# 多元线性回归：分析所有广告渠道的综合影响
model_all = smf.ols(formula='Sales ~ TV + Radio + Newspaper', data=df).fit()
print("\n\n=== 多元回归（全渠道）摘要 ===")
print(model_all.summary())

# 交互效应分析：检验TV与广播的组合投放效果
model_interact = smf.ols(formula='Sales ~ TV * Radio + Newspaper', data=df).fit()
print("\n\n=== 回归摘要（含交互项）===")
print(model_interact.summary())

# 回归诊断：残差图评估模型假设合理性
sm.graphics.plot_regress_exog(model_all, 'TV')

plt.tight_layout()
plt.show()