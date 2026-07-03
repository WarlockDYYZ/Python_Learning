import pandas as pd
import numpy as np

# 生成带缺失值的多变量时序样本：电力负荷+气温+节假日
rng = pd.date_range("2024-01-01", periods=1000, freq="h")
df = pd.DataFrame({
    "power_load": 1000 + np.linspace(0, 100, 1000) + 50*np.sin(np.linspace(0, 20*np.pi, 1000)) + np.random.normal(0, 10, 1000),
    "temperature": np.random.normal(loc=20, scale=5, size=1000),
    "is_holiday": np.random.randint(0, 2, size=1000)
}, index=rng)
# 人为制造3段典型缺失区间：短、中、长区间
df.loc["2024-01-05 08:00":"2024-01-05 10:00", "power_load"] = np.nan  # 短区间（3小时）
df.loc["2024-01-10 12:00":"2024-01-10 20:00", "power_load"] = np.nan  # 中区间（9小时）
df.loc["2024-01-15 00:00":"2024-01-17 00:00", "power_load"] = np.nan  # 长区间（48小时）
print(df)


# 短区间缺失值填充
# # 方案1：前向填充，适用于短间隔、无突变的时序场景
# df_ffill = df.copy()
# df_ffill["power_load"] = df_ffill["power_load"].ffill(limit=3)  # 限制最大填充间隔，避免扩散错误

# 方案2：时间加权线性插值，考虑时间戳距离，比普通线性插值更精准
df_linear = df.copy()
df_linear["power_load"] = df_linear["power_load"].interpolate(method="time")


# 中长区间缺失值填充
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.seasonal import STL

# 方案1：SARIMAX模型预测填充，适配含季节趋势的中区间缺失
# 拆分非缺失训练数据、缺失预测区间
train_data = df.loc[df["power_load"].notna(), "power_load"]
missing_start = "2024-01-10 12:00"
missing_end = "2024-01-10 20:00"
# 训练SARIMAX模型，结合外生变量（气温、节假日）提升精度
model = SARIMAX(
    endog=train_data,
    exog=df.loc[train_data.index, ["temperature", "is_holiday"]],
    order=(1,1,1),
    seasonal_order=(1,1,1,24)  # 日季节周期，小时级数据周期为24
)
model_fit = model.fit(disp=False)
# 预测缺失区间数值
exog_pred = df.loc[missing_start:missing_end, ["temperature", "is_holiday"]]
pred = model_fit.predict(start=missing_start, end=missing_end, exog=exog_pred)
# 填充缺失值
df_sarimax = df.copy()
df_sarimax.loc[missing_start:missing_end, "power_load"] = pred

# # 方案2：STL分解填充，适配长区间缺失（提取趋势+季节项，叠加残差插值）
# stl = STL(df["power_load"].interpolate(method="time"), period=24)
# res = stl.fit()
# # 趋势项插值、季节项复用周期规律，叠加残差插值得到填充值
# df_stl = df.copy()
# df_stl.loc[df_stl["power_load"].isna(), "power_load"] = (
#     res.trend.interpolate(method="time") +
#     res.seasonal.ffill() +
#     res.resid.interpolate(method="time")
# )


# 多变量长区间缺失值填充
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer, KNNImputer
from sklearn.preprocessing import StandardScaler

# 准备特征集：将时间戳拆解为周期特征，补充关联变量
df_ml = df.copy()
# 提取时间周期特征（小时、星期几、是否工作日），捕捉季节规律
df_ml["hour"] = df_ml.index.hour
df_ml["weekday"] = df_ml.index.weekday
df_ml["is_workday"] = df_ml["weekday"].isin([0,1,2,3,4]).astype(int)

# 方案1：KNN填充，基于相似时间点的样本填充
knn_imputer = KNNImputer(n_neighbors=5, weights="distance")
df_ml_knn = pd.DataFrame(
    knn_imputer.fit_transform(df_ml),
    columns=df_ml.columns,
    index=df_ml.index
)

# 方案2：MICE多重填充，迭代建模，考虑变量间的互相关关系
mice_imputer = IterativeImputer(max_iter=50, random_state=42)
df_ml_mice = pd.DataFrame(
    mice_imputer.fit_transform(df_ml),
    columns=df_ml.columns,
    index=df_ml.index
)


















