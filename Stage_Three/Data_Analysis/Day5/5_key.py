import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stl._stl import STL

# 1. 数据加载与重采样：从15分钟级下采样到小时级
df_raw = pd.read_csv("power_load_raw.csv", index_col="timestamp", parse_dates=["timestamp"])
df_hourly = df_raw.resample("h", closed="left", label="left").agg(
    load_avg=("power_load", "mean"),
    load_max=("power_load", "max"),
    temperature=("temperature", "mean"),
    is_holiday=("is_holiday", "max")
)

# 2. 缺失值分层填充：适配不同缺失区间
# 短区间：Pandas前向填充
df_hourly["load_avg"] = df_hourly["load_avg"].ffill(limit=3)
# 中区间：Statsmodels SARIMAX预测填充
# 长区间：STL分解+季节趋势填充

# 3. 时序分解：验证日/周季节趋势，确认模型选型
stl = STL(df_hourly["load_avg"], period=24)  # 小时级数据，日周期s=24
res = stl.fit()
res.plot()  # 观察趋势、季节、残差项分布，确认平稳性

# 4. 多模型训练：对比SARIMAX、GradientBoosting、混合模型performance
# 方案1：SARIMAX，捕捉线性季节趋势
model_sarimax = SARIMAX(
    endog=train["load_avg"],
    exog=train[["temperature", "is_holiday"]],
    order=(1,1,1),
    seasonal_order=(1,1,1,24)
)
# 方案2：GradientBoosting，捕捉非线性外生变量关系
# 方案3：混合模型：用SARIMAX提取趋势项，用GradientBoosting拟合残差
residuals = train["load_avg"] - model_sarimax.fittedvalues
# 用树模型拟合残差的非线性波动，叠加到统计模型预测结果中

# 5. 滚动预测：生成未来7天的小时级负荷预测
# 先获取未来7天的外生变量 forecast data (temperature, is_holiday)
future_exog = pd.read_csv("future_weather.csv", index_col="timestamp", parse_dates=["timestamp"])
# 混合模型滚动预测
predictions = []
for i in range(0, 7*24, 24):
    # 用前序窗口数据更新模型
    model_sarimax = SARIMAX(
        endog=df_hourly["load_avg"].iloc[:-len(future_exog)+i],
        exog=df_hourly[["temperature", "is_holiday"]].iloc[:-len(future_exog)+i],
        order=(1,1,1),
        seasonal_order=(1,1,1,24)
    )
    # 预测当前24小时结果
    pred_sarimax = model_sarimax.get_forecast(steps=24, exog=future_exog.iloc[i:i+24]).predicted_mean
    pred_gbr = best_gbr_model.predict(future_features.iloc[i:i+24])
    # 叠加混合模型结果：统计趋势+非线性残差
    pred_combined = pred_sarimax + pred_gbr
    predictions.extend(pred_combined)