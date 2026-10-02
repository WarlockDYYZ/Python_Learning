"""D3: 指标计算模块

提供核心业务指标计算：GMV汇总、CTR、CPC、新增用户、周环比等。
"""
import pandas as pd
import numpy as np


def calc_channel_summary(df: pd.DataFrame) -> pd.DataFrame:
    """按渠道汇总核心指标

    Args:
        df: 筛选后的数据

    Returns:
        渠道汇总表
    """
    summary = df.groupby("channel").agg(
        total_gmv=("gmv", "sum"),
        total_exposure=("exposure", "sum"),
        total_clicks=("clicks", "sum"),
        total_cost=("cost", "sum"),
        total_new_users=("new_users", "sum"),
        days=("date", "nunique"),
    ).reset_index()

    # 计算衍生指标
    summary["ctr"] = np.where(summary["total_exposure"] > 0,
                              summary["total_clicks"] / summary["total_exposure"] * 100, 0)
    summary["cpc"] = np.where(summary["total_clicks"] > 0,
                              summary["total_cost"] / summary["total_clicks"], 0)
    summary["gmv_per_user"] = np.where(summary["total_new_users"] > 0,
                                       summary["total_gmv"] / summary["total_new_users"], 0)
    summary["avg_daily_gmv"] = summary["total_gmv"] / summary["days"]

    return summary


def calc_weekly_comparison(df: pd.DataFrame) -> pd.DataFrame:
    """计算周环比对比

    将数据按自然周分组，计算每周各渠道的GMV及环比变化。

    Args:
        df: 筛选后的数据（date列为datetime）

    Returns:
        周度对比表
    """
    df_copy = df.copy()
    df_copy["week"] = df_copy["date"].dt.isocalendar().week.astype(int)
    df_copy["year_week"] = df_copy["date"].dt.strftime("%Y-W%U")

    weekly = df_copy.groupby(["year_week", "channel"]).agg(
        weekly_gmv=("gmv", "sum"),
        weekly_clicks=("clicks", "sum"),
        weekly_cost=("cost", "sum"),
    ).reset_index()

    # 计算环比
    weekly = weekly.sort_values(["year_week", "channel"])
    weekly["prev_gmv"] = weekly.groupby("channel")["weekly_gmv"].shift(1)
    weekly["gmv_woq"] = np.where(
        weekly["prev_gmv"].notna() & weekly["prev_gmv"] > 0,
        (weekly["weekly_gmv"] - weekly["prev_gmv"]) / weekly["prev_gmv"] * 100,
        None
    )

    return weekly


def calc_top_channels(df: pd.DataFrame, top_n=3) -> pd.DataFrame:
    """获取TOP N渠道（按GMV排序）

    Args:
        df: 筛选后的数据
        top_n: TOP数量

    Returns:
        TOP渠道表
    """
    channel_gmv = df.groupby("channel")["gmv"].sum().sort_values(ascending=False)
    return channel_gmv.head(top_n)


def calc_daily_trend(df: pd.DataFrame) -> pd.DataFrame:
    """计算每日汇总趋势

    Args:
        df: 筛选后的数据

    Returns:
        日趋势表
    """
    daily = df.groupby("date").agg(
        daily_gmv=("gmv", "sum"),
        daily_clicks=("clicks", "sum"),
        daily_cost=("cost", "sum"),
        daily_exposure=("exposure", "sum"),
    ).reset_index()

    daily["daily_ctr"] = np.where(daily["daily_exposure"] > 0,
                                  daily["daily_clicks"] / daily["daily_exposure"] * 100, 0)
    return daily