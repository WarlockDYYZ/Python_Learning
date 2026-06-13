import numpy as np
import optuna
from sklearn import metrics
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from optuna.visualization import plot_optimization_history, plot_param_importances
from xgboost.callback import EarlyStopping


np.random.seed(42)
n_samples = 1000
X = np.random.randn(n_samples, 8)   # 8个特征
y = X[:,0] * 2.5 + X[:,2] * 1.2 + np.random.normal(0, 1, n_samples)

# 划分训练集、测试集、验证集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)


# 定义目标函数：Optuna将在该函数定义的参数空间内寻找最优解
def objective(trial):
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 100, 1000, step=50),
        "max_depth": trial.suggest_int("max_depth", 2, 10),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3, log=True),
        "subsample": trial.suggest_float("subsample", 0.5, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
        "gamma": trial.suggest_float("gamma", 0, 5),
        "random_state": 42
    }

    model = XGBRegressor(**params)
    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        verbose=False
    )
    y_pred_val = model.predict(X_val)
    val_mse = mean_squared_error(y_val, y_pred_val)
    return val_mse


# 创建Study对象，启动优化过程
study = optuna.create_study(direction='minimize')  # 最小化验证集MSE
study.optimize(objective, n_trials=100, show_progress_bar=True)

# 输出最优参数
print("Best parameters:", study.best_params)

# 用最优参数重新训练模型，评估测试集表现
best_model = XGBRegressor(**study.best_params, random_state=42)
best_model.fit(X_train, y_train)
y_pred_test = best_model.predict(X_test)

# 打印测试集评价指标
print("n测试集评估结果：")
print(f"均方误差(MSE): {mean_squared_error(y_test, y_pred_test):.4f}")
print(f"均方根误差(RMSE): {np.sqrt(mean_squared_error(y_test, y_pred_test)):.4f}")
print(f"平均绝对误差(MAE): {metrics.mean_absolute_error(y_test, y_pred_test):.4f}")
print(f"拟合优度(R²): {r2_score(y_test, y_pred_test):.4f}")

# 可视化调优过程
plot_optimization_history(study).show()  # 优化历史收敛趋势
plot_param_importances(study).show()  # 超参数重要性贡献