import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import RandomizedSearchCV, TimeSeriesSplit

import numpy as np


# 1. 时序特征工程：将时序转化为监督学习数据集
def create_timeseries_features(df, target_col, lags=24, window_sizes=[24, 72]):
    """生成滞后特征、滚动统计特征、时间周期特征"""
    df_fe = df.copy()
    # 1.1 生成目标变量滞后特征
    for lag in range(1, lags+1):
        df_fe[f"lag_{lag}"] = df_fe[target_col].shift(lag)
    # 1.2 生成滚动窗口统计特征
    for window in window_sizes:
        df_fe[f"rolling_mean_{window}"] = df_fe[target_col].shift(1).rolling(window=window).mean()
        df_fe[f"rolling_std_{window}"] = df_fe[target_col].shift(1).rolling(window=window).std()
        df_fe[f"rolling_max_{window}"] = df_fe[target_col].shift(1).rolling(window=window).max()
    # 1.3 生成时间周期特征（三角函数编码）
    df_fe["hour_sin"] = np.sin(2 * np.pi * df_fe.index.hour / 24)
    df_fe["hour_cos"] = np.cos(2 * np.pi * df_fe.index.hour / 24)
    df_fe["weekday_sin"] = np.sin(2 * np.pi * df_fe.index.weekday / 7)
    df_fe["weekday_cos"] = np.cos(2 * np.pi * df_fe.index.weekday / 7)
    # 1.4 删除缺失值（由滞后、滚动特征生成的空值）
    df_fe = df_fe.dropna()
    return df_fe

df = pd.read_csv("教程只给了代码并没有给示例数据.csv")
# 生成特征集
df_fe = create_timeseries_features(df, target_col="power_load")
# 划分特征集X、目标变量y
X = df_fe.drop("power_load", axis=1)
y = df_fe["power_load"]

# 时序划分训练集、测试集
train_size = int(len(X) * 0.8)
X_train, X_test = X.iloc[:train_size], X.iloc[train_size:]
y_train, y_test = y.iloc[:train_size], y.iloc[train_size:]

# 2. 搭建模型 pipeline：标准化+梯度提升树，组合特征预处理与模型训练
pipeline = Pipeline([
    ("scaler", StandardScaler()),  # 标准化特征，适配树模型的分裂逻辑
    ("gbr", GradientBoostingRegressor(loss="absolute_error", random_state=42))
])

# 3. 随机搜索调参：配合时序交叉验证，优化模型超参数
param_dist = {
    "gbr__n_estimators": [100, 200, 300],
    "gbr__max_depth": [3, 5, 7],
    "gbr__learning_rate": [0.01, 0.05, 0.1],
    "gbr__subsample": [0.7, 0.8, 0.9]
}
# 用TimeSeriesSplit做时序交叉验证，避免数据泄露
tscv = TimeSeriesSplit(n_splits=5, test_size=24)
random_search = RandomizedSearchCV(
    pipeline,
    param_distributions=param_dist,
    n_iter=20,
    cv=tscv,
    scoring="neg_mean_absolute_error",
    n_jobs=-1,
    random_state=42
)
random_search.fit(X_train, y_train)
best_model = random_search.best_estimator_
print("最优模型参数：", random_search.best_params_)

# 4. 预测与模型校验
# 预测结果
y_pred = best_model.predict(X_test)
# 平均绝对误差
mae = mean_absolute_error(y_test, y_pred)
# 根均方误差
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
# 平均绝对百分比误差
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
print(f"测试集MAE：{mae:.2f}，RMSE：{rmse:.2f}，MAPE：{mape:.2f}%")