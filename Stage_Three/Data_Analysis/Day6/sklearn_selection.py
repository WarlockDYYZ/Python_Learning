import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


# 模拟业务数据集
# 固定随机种子，保证结果可复现
np.random.seed(42)
# 模拟10000条电商用户行为数据
df = pd.DataFrame({
    # 低基数无序特征：支付方式
    "pay_type": np.random.choice(["微信", "支付宝", "银行卡"], size=10000),
    # 低基数有序特征：会员等级（业务顺序：青铜<白银<黄金<钻石）
    "user_level": np.random.choice(["青铜", "白银", "黄金", "钻石"], size=10000),
    # 高基数无序特征：商品类目（50个类别）
    "goods_category": np.random.choice([f"cat_{i}" for i in range(50)], size=10000),
    # 数值特征：页面浏览量、加购次数、收藏次数
    "pv": np.random.randint(1, 100, size=10000),
    "cart": np.random.randint(0, 50, size=10000),
    "fav": np.random.randint(0, 20, size=10000),
    # 目标变量：日销售额（连续型）
    "sales": np.random.randint(10, 1000, size=10000)
})

# 拆分特征集、目标变量
X = df.drop("sales", axis=1)
y = df["sales"]
# 先拆分训练集、测试集，后续编码/筛选仅基于训练集拟合
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# 构建特征工程流水线
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
from sklearn.feature_selection import VarianceThreshold, SelectFromModel, RFECV
from sklearn.ensemble import RandomForestRegressor
from category_encoders import TargetEncoder

# 1. 划分特征类型，匹配编码方案
cat_ordinal = ["user_level"]       # 低基数有序特征
cat_low_nominal = ["pay_type"]     # 低基数无序特征
cat_high_nominal = ["goods_category"]  # 高基数无序特征
num_cols = ["pv", "cart", "fav"]   # 数值特征，直接保留

# 2. 构建编码转换器：对不同类型特征分别处理
preprocessor = ColumnTransformer(transformers=[
    # 有序编码：手动指定业务等级顺序，避免默认字母序乱序
    ("ord", OrdinalEncoder(categories=[["青铜", "白银", "黄金", "钻石"]]), cat_ordinal),
    # 独热编码：drop_first规避虚拟变量陷阱，handle_unknown忽略测试集未知类别
    ("ohe", OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore"), cat_low_nominal),
    # 目标编码：高基数特征，smoothing抑制稀有类别过拟合
    ("te", TargetEncoder(smoothing=10), cat_high_nominal),
    # 数值特征：原封不动保留
    ("num", "passthrough", num_cols)
])

# 3. 构建完整筛选流水线：粗筛选→精筛选→模型
pipeline = Pipeline(steps=[
    # 编码预处理
    ("preprocessor", preprocessor),
    # 粗筛选：方差过滤，剔除方差≤0.01的无意义特征
    ("var_filter", VarianceThreshold(threshold=0.01)),
    # 精筛选1：嵌入式筛选，剔除重要性低于中位数的特征
    ("select_efm", SelectFromModel(
        RandomForestRegressor(n_estimators=100, random_state=42),
        threshold="median"
    )),
    # 精筛选2：包裹式RFECV交叉验证，自动确定最优特征数量
    ("select_rfecv", RFECV(
        estimator=RandomForestRegressor(n_estimators=50, random_state=42),
        step=1,
        cv=5,
        scoring="r2",
        n_jobs=-1
    )),
    # 最终预测模型
    ("model", RandomForestRegressor(n_estimators=100, random_state=42))
])

# 4. 训练流水线：仅用训练集拟合，自动完成所有编码、筛选、模型训练
pipeline.fit(X_train, y_train)


# 查看筛选结果与模型效果
from sklearn.metrics import r2_score, mean_absolute_error

# 提取所有编码后的特征名
encoded_cols = pipeline.named_steps["preprocessor"].get_feature_names_out()
# 获取RFECV筛选后保留的特征布尔掩码
selected_mask = pipeline.named_steps["select_rfecv"].get_support()
# 过滤得到最终保留的核心特征
selected_features = encoded_cols[selected_mask]
print("筛选后的核心业务特征列表：", selected_features)

# 测试集预测
y_pred = pipeline.predict(X_test)
# 模型回归效果评估
print(f"测试集R2得分：{r2_score(y_test, y_pred):.4f}")
print(f"测试集MAE得分：{mean_absolute_error(y_test, y_pred):.4f}")