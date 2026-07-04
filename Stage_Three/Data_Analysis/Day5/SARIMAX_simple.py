import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.model_selection import TimeSeriesSplit
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error

# 1. 准备多变量时序数据：电力负荷（目标变量）+气温+节假日（外生变量）
df = pd.read_csv(
    "power_load.csv",
    index_col="timestamp",
    parse_dates=["timestamp"]
)
# 划分训练集、测试集：按时间顺序划分，前80%为训练集，后20%为测试集
train_size = int(len(df) * 0.8)
train = df.iloc[:train_size]
test = df.iloc[train_size:]

# 2. 平稳性检验：ADF检验，确认差分阶数d
adf_result = sm.tsa.adfuller(train["power_load"])
print("ADF检验P值：", adf_result[1])
# 若P值≥0.05，执行1阶差分，再重新检验

# 3. 模型训练：SARIMAX搭配外生变量，组合参数通过AIC信息准则筛选
model = SARIMAX(
    endog=train["power_load"],  # 目标变量：单变量时序
    exog=train[["temperature", "is_holiday"]],  # 外生变量：多维度影响因素
    order=(1,1,1),  # 非季节阶数，根据PACF/ACF图定阶
    seasonal_order=(1,1,1,24),  # 季节阶数：小时级数据，日周期s=24
    enforce_stationarity=False,
    enforce_invertibility=False
)
model_fit = model.fit(disp=False)
print(model_fit.summary())

# 4. 滚动交叉验证：评估模型泛化能力
# 用TimeSeriesSplit实现滚动划分，避免数据泄露
tscv = TimeSeriesSplit(n_splits=5, test_size=24)  # 5折交叉验证，每折测试集为24小时
cv_scores = []
for train_idx, val_idx in tscv.split(train):
    # 切分每一折数据
    cv_train = train.iloc[train_idx]
    cv_val = train.iloc[val_idx]
    # 在当前折上训练 SARIMAX 模型
    cv_model = SARIMAX(
        endog=cv_train["power_load"],  # 当前折训练集中的内生变量（目标变量）
        exog=cv_train[["temperature", "is_holiday"]],  # 当前折训练集中的外生变量（外部影响因素）
        order=(1,1,1),
        # 定义非季节性的 ARIMA 参数 (p, d, q)；
        # p=1：自回归阶数（AR），使用 1 个滞后的值来预测当前值。
        # d = 1：差分阶数（I），对数据进行 1 阶差分以消除趋势，使其平稳。
        # q = 1：移动平均阶数（MA），使用 1 个滞后的预测误差来修正当前预测。
        seasonal_order=(1,1,1,24)
        # s=24：季节周期长度。因为是小时级数据，一天有 24 个小时，所以设定为 24。
        # P、D、Q 与上面相同
    )
    cv_fit = cv_model.fit(disp=False)
    cv_pred = cv_fit.predict(
        start=cv_val.index[0],
        end=cv_val.index[-1],
        exog=cv_val[["temperature", "is_holiday"]]
    )
    cv_scores.append(np.sqrt(mean_squared_error(cv_val["power_load"], cv_pred)))
print("交叉验证平均RMSE：", np.mean(cv_scores))

# 5. 样本外预测：对测试集生成预测结果
predictions = model_fit.get_forecast(
    steps=len(test),
    exog=test[["temperature", "is_holiday"]]
).predicted_mean

# 6. 模型校验：计算预测指标、残差白噪声检验
mae = mean_absolute_error(test["power_load"], predictions)
rmse = np.sqrt(mean_squared_error(test["power_load"], predictions))
mape = np.mean(np.abs((test["power_load"] - predictions) / test["power_load"])) * 100
print(f"测试集MAE：{mae:.2f}，RMSE：{rmse:.2f}，MAPE：{mape:.2f}%")

# 残差白噪声检验：若P值>0.05，说明残差为白噪声，模型已提取所有有效信息
resid_test = sm.stats.acorr_ljungbox(model_fit.resid, lags=[12], return_df=True)
print("残差白噪声检验P值：", resid_test["lb_pvalue"].values[0])