import statsmodels.api as sm
import pandas as pd
import numpy as np


# 创建模拟用户数据
np.random.seed(42)
n_samples = 200
data = pd.DataFrame({
    'age': np.random.randint(18, 65, n_samples),
    'income': np.random.randint(20000, 150000, n_samples)
})
# 构造购买概率（受年龄、收入正向影响）
data['buy_prob'] = 1 / (1 + np.exp(-(-10 + 0.1*data['age'] + 0.00005*data['income'] + np.random.normal(0, 1.5, n_samples))))
data['purchased'] = np.random.binomial(1, data['buy_prob'])

# 构建逻辑回归模型（GLM指定二项分布族）
X = data[['age', 'income']]
X = sm.add_constant(X)  # 添加截距项
y = data['purchased']
logit_model = sm.GLM(y, X, family=sm.families.Binomial()).fit()
print(logit_model.summary())

# 计算赔率比（Odds Ratios），直观解释特征影响
odds_ratios = np.exp(logit_model.params)
print("n各特征的赔率比：")
print(odds_ratios)