"""D2: 数据筛选模块

提供灵活的日期和渠道筛选函数，支持边界条件处理。
"""
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def filter_by_date(df: pd.DataFrame, start_date=None, end_date=None) -> pd.DataFrame:
    """按日期范围筛选

    Args:
        df: 输入DataFrame（需含date列）
        start_date: 起始日期（含），str或datetime
        end_date: 结束日期（含），str或datetime

    Returns:
        筛选后的DataFrame
    """
    mask = pd.Series(True, index=df.index)

    if start_date is not None:
        start_dt = pd.to_datetime(start_date)
        mask &= df["date"] >= start_dt
        logger.info(f"日期筛选 >= {start_date}: 保留 {mask.sum()} 行")

    if end_date is not None:
        end_dt = pd.to_datetime(end_date)
        mask &= df["date"] <= end_dt
        logger.info(f"日期筛选 <= {end_date}: 保留 {mask.sum()} 行")

    return df[mask].reset_index(drop=True)


def filter_by_channel(df: pd.DataFrame, channels=None) -> pd.DataFrame:
    """按渠道筛选

    Args:
        df: 输入DataFrame（需含channel列）
        channels: 渠道列表，None表示不筛选

    Returns:
        筛选后的DataFrame

    Raises:
        ValueError: 所选渠道在数据中不存在
    """
    if channels is None:
        return df

    allowed = set(channels) & set(df["channel"].unique())
    if not allowed:
        available = sorted(df["channel"].unique())
        raise ValueError("所选渠道 {} 无数据，可用渠道: {}".format(channels, available))

    # 记录未找到的渠道
    not_found = set(channels) - set(df["channel"].unique())
    if not_found:
        logger.warning(f"以下渠道在数据中不存在: {not_found}")

    mask = df["channel"].isin(allowed)
    logger.info(f"渠道筛选 {sorted(allowed)}: 保留 {mask.sum()} 行")
    return df[mask].reset_index(drop=True)


def filter_df(df: pd.DataFrame, start_date=None, end_date=None, channels=None) -> pd.DataFrame:
    """组合筛选：日期 + 渠道

    串联应用日期筛选和渠道筛选，最终去除重复行。

    Args:
        df: 输入DataFrame
        start_date: 起始日期
        end_date: 结束日期
        channels: 渠道列表

    Returns:
        筛选后的DataFrame

    Raises:
        AssertionError: 筛选结果为空时抛出
    """
    result = filter_by_date(df, start_date, end_date)
    result = filter_by_channel(result, channels)
    result = result.drop_duplicates().reset_index(drop=True)

    assert not result.empty, "筛选结果为空，请检查日期/渠道范围"
    logger.info(f"最终筛选结果: {len(result)} 行")
    return result