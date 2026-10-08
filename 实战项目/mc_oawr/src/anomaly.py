"""D4: 异常检测模块

提供基于MAD(中位数绝对偏差)和IQR方法的异常检测，
阈值外置配置文件，支持日志记录。
"""
import os
import logging
import yaml
import pandas as pd
import numpy as np

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("logs/run.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_rules(config_path=None):
    """加载异常检测规则配置

    Args:
        config_path: 配置文件路径，默认使用config/rules.yaml

    Returns:
        规则配置dict
    """
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), "..", "config", "rules.yaml")

    with open(config_path, "r", encoding="utf-8") as f:
        rules = yaml.safe_load(f)

    logger.info(f"已加载异常检测规则: {list(rules.get('channel_rules', {}).keys())}")
    return rules


def detect_anomaly_mad(series, k=3):
    """MAD(中位数绝对偏差)异常检测

    原理: 计算每个值与中位数的偏差，超过 k * MAD 的视为异常。
    MAD = median(|Xi - median(X)|) * 1.4826 (一致性修正因子)

    Args:
        series: 数值序列
        k: 阈值倍数，默认3

    Returns:
        异常布尔掩码
    """
    center = series.median()
    mad = (series - center).abs().median() * 1.4826
    return (series - center).abs() > k * max(mad, 1e-6)


def detect_anomaly_iqr(series, k=1.5):
    """IQR(四分位距)异常检测

    原理: Q1 - k*IQR 以下 或 Q3 + k*IQR 以上的值视为异常。

    Args:
        series: 数值序列
        k: 阈值倍数，默认1.5

    Returns:
        异常布尔掩码
    """
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    return (series < q1 - k * iqr) | (series > q3 + k * iqr)


def detect_anomalies(df, rules=None, config_path=None):
    """检测异常数据行

    按渠道分别应用对应的检测规则，全局规则作为兜底。

    Args:
        df: 筛选后的销售数据
        rules: 规则配置dict，None则从文件加载
        config_path: 配置文件路径

    Returns:
        异常数据DataFrame，包含原始列 + rule(检测方法) + deviation(偏离度)列
    """
    if rules is None:
        rules = load_rules(config_path)

    channel_rules = rules.get("channel_rules", {})
    global_rule = rules.get("global", {"method": "iqr", "k": 1.5})

    all_anomalies = []

    for channel, grp in df.groupby("channel"):
        # 获取该渠道的检测规则
        ch_rule = channel_rules.get(channel, global_rule)
        method = ch_rule["method"]
        k = ch_rule["k"]

        # 选择检测方法
        if method == "mad":
            mask = detect_anomaly_mad(grp["gmv"], k=k)
        elif method == "iqr":
            mask = detect_anomaly_iqr(grp["gmv"], k=k)
        else:
            logger.warning(f"未知检测方法: {method}，使用iqr")
            mask = detect_anomaly_iqr(grp["gmv"], k=k)

        # 记录异常行
        anomaly_rows = grp[mask]
        if len(anomaly_rows) > 0:
            logger.warning(
                f"渠道[{channel}] 检测到 {len(anomaly_rows)} 个异常值 "
                f"(method={method}, k={k})"
            )

            # 计算偏离度
            center = grp["gmv"].median()
            spread = (grp["gmv"] - center).abs().median() * 1.4826
            deviations = (anomaly_rows["gmv"] - center).abs() / max(spread, 1e-6)

            anomaly_data = anomaly_rows.copy()
            anomaly_data["rule"] = method
            anomaly_data["deviation"] = deviations.values
            all_anomalies.append(anomaly_data)

    if all_anomalies:
        result = pd.concat(all_anomalies, ignore_index=True)
        # 重排列顺序
        cols = ["date", "channel", "exposure", "clicks", "cost", "gmv", "new_users", "rule", "deviation"]
        existing_cols = [c for c in cols if c in result.columns]
        result = result[existing_cols]
        logger.info(f"共检测到 {len(result)} 条异常记录")
        return result
    else:
        logger.info("未检测到异常数据")
        return pd.DataFrame(columns=["date", "channel", "gmv", "rule", "deviation"])


def detect_anomalies_global(df, rules=None):
    """全局异常检测（不按渠道分组）

    Args:
        df: 筛选后的销售数据
        rules: 规则配置

    Returns:
        异常数据DataFrame
    """
    if rules is None:
        rules = load_rules()

    global_rule = rules.get("global", {"method": "iqr", "k": 1.5})
    method = global_rule["method"]
    k = global_rule["k"]

    if method == "mad":
        mask = detect_anomaly_mad(df["gmv"], k=k)
    else:
        mask = detect_anomaly_iqr(df["gmv"], k=k)

    if mask.any():
        anomalies = df[mask].copy()
        center = df["gmv"].median()
        spread = (df["gmv"] - center).abs().median() * 1.4826
        anomalies["rule"] = method
        anomalies["deviation"] = (anomalies["gmv"] - center).abs() / max(spread, 1e-6)
        logger.info(f"全局检测: {len(anomalies)} 条异常记录")
        return anomalies
    else:
        logger.info("全局检测未发现问题")
        return pd.DataFrame(columns=["date", "channel", "gmv", "rule", "deviation"])