from statsmodels.stats.outliers_influence import variance_inflation_factor
import seaborn as sns
import pandas as pd
import statsmodels.api as sm


df = sns.load_dataset('titanic')

# 构造待检验特征矩阵
X = df[['age', 'pclass', 'fare', 'sibsp', 'parch']]
# 计算 VIF 之前，必须确保特征矩阵中没有任何 NaN 或 inf，因为数据集中只有 NaN，所以仅处理 NaN
X = X.dropna()
X = sm.add_constant(X)  # 必须添加常数项，适配VIF计算逻辑

# 批量计算VIF值
vif_data = pd.DataFrame()
vif_data["feature"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
print(vif_data)

# 筛选重度共线性特征（VIF>10）
high_vif = vif_data[vif_data['VIF'] > 10]
print("需要剔除的高共线性特征：", high_vif)