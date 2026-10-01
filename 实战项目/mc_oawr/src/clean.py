"""D2: 数据清洗模块

提供数据清洗函数：去重、处理缺失值、日期类型转换、类型校验。
"""
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """清洗销售数据

    处理步骤:
    1. 去除完全重复行
    2. 日期列转为datetime
    3. 数值列类型校验
    4. 处理缺失值（gmv列用渠道中位数填充）

    Args:
        df: 原始销售数据DataFrame

    Returns:
        清洗后的DataFrame
    """
    initial_rows = len(df)
    logger.info(f"开始清洗数据，初始行数: {initial_rows}")

    # 1. 去重
    dup_mask = df.duplicated(keep=False)
    n_dups = dup_mask.sum()
    df = df.drop_duplicates(keep="first").reset_index(drop=True)
    logger.info(f"去除重复行: {n_dups} 行")

    # 2. 日期列转换
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    null_dates = df["date"].isna().sum()
    if null_dates > 0:
        logger.warning(f"存在 {null_dates} 个无法解析的日期，已标记为NaT")

    # 删除日期为NaT的行
    df = df.dropna(subset=["date"]).reset_index(drop=True)

    # 3. 数值列类型转换
    for col in ["exposure", "clicks", "new_users"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    df["cost"] = pd.to_numeric(df["cost"], errors="coerce").fillna(0.0)

    # 4. GMV缺失值处理：用同渠道的中位数填充
    gmv_null_before = df["gmv"].isna().sum()
    if gmv_null_before > 0:
        median_gmv = df.groupby("channel")["gmv"].transform("median")
        df["gmv"] = df["gmv"].fillna(median_gmv)
        logger.info(f"使用渠道中位数填充 {gmv_null_before} 个GMV缺失值")

    # 5. 负值检查
    neg_gmv = (df["gmv"] < 0).sum()
    if neg_gmv > 0:
        logger.warning(f"存在 {neg_gmv} 个负值GMV，已设为0")
        df.loc[df["gmv"] < 0, "gmv"] = 0

    logger.info(f"清洗完成，最终行数: {len(df)}")
    return df


def load_and_clean(csv_path: str) -> pd.DataFrame:
    """加载CSV并清洗

    Args:
        csv_path: CSV文件路径

    Returns:
        清洗后的DataFrame
    """
    df = pd.read_csv(csv_path)
    df = clean_sales_data(df)
    return df