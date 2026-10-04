"""D3: 可视化图表模块

提供图表渲染函数，包含中文支持、样式配置、防遮挡等调试处理。
"""
import os
import json
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from datetime import datetime

# 中文支持配置
plt.rcParams["font.sans-serif"] = ["WenQuanYi Zen Hei", "SimHei", "Microsoft YaHei", "Noto Sans CJK SC"]
plt.rcParams["axes.unicode_minus"] = False

# 加载样式配置
_config_path = os.path.join(os.path.dirname(__file__), "..", "config", "style.json")
with open(_config_path, "r", encoding="utf-8") as f:
    STYLE = json.load(f)


def _get_colors(n=5):
    """获取配色方案"""
    colors = STYLE.get("colors", ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#3B1F2B"])
    return [colors[i % len(colors)] for i in range(n)]


def plot_daily_gmv_trend(daily_df, save_path=None):
    """绘制每日GMV趋势折线图

    Args:
        daily_df: 日趋势数据（含date和daily_gmv列）
        save_path: 保存路径
    """
    fig, ax = plt.subplots(figsize=(STYLE["chart_width"], STYLE["chart_height"]))

    ax.plot(daily_df["date"], daily_df["daily_gmv"],
            color=_get_colors()[0], linewidth=2, marker="", label="日GMV")
    ax.fill_between(daily_df["date"], daily_df["daily_gmv"], alpha=0.1, color=_get_colors()[0])

    # 移动平均线
    if len(daily_df) > 7:
        ma7 = daily_df["daily_gmv"].rolling(7).mean()
        ax.plot(daily_df["date"], ma7, color=_get_colors()[1], linewidth=1.5,
                linestyle="--", label="7日移动平均")

    ax.set_title("每日GMV趋势", fontsize=STYLE["title_fontsize"], fontweight="bold")
    ax.set_xlabel("日期", fontsize=STYLE["label_fontsize"])
    ax.set_ylabel("GMV", fontsize=STYLE["label_fontsize"])
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
    ax.tick_params(axis="x", rotation=45, labelsize=STYLE["tick_fontsize"])
    ax.legend(loc="upper right", fontsize=STYLE["tick_fontsize"])
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=STYLE["dpi"], bbox_inches="tight")
    plt.close(fig)
    return save_path


def plot_channel_comparison(channel_summary, save_path=None):
    """绘制渠道GMV对比柱状图

    Args:
        channel_summary: 渠道汇总表
        save_path: 保存路径
    """
    df = channel_summary.sort_values("total_gmv", ascending=True)

    fig, ax = plt.subplots(figsize=(STYLE["chart_width"], STYLE["chart_height"]))
    colors = _get_colors(len(df))
    bars = ax.barh(df["channel"], df["total_gmv"], color=colors, edgecolor="white", height=0.6)

    # 在柱子末端添加数值标签
    for bar, val in zip(bars, df["total_gmv"]):
        ax.text(bar.get_width() + df["total_gmv"].max() * 0.02,
                bar.get_y() + bar.get_height() / 2,
                f"{val:.0f}", va="center", fontsize=STYLE["tick_fontsize"])

    ax.set_title("各渠道GMV对比", fontsize=STYLE["title_fontsize"], fontweight="bold")
    ax.set_xlabel("GMV", fontsize=STYLE["label_fontsize"])
    ax.grid(True, axis="x", alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=STYLE["dpi"], bbox_inches="tight")
    plt.close(fig)
    return save_path


def plot_channel_ctr_bar(channel_summary, save_path=None):
    """绘制渠道CTR对比图

    Args:
        channel_summary: 渠道汇总表（含ctr列）
        save_path: 保存路径
    """
    df = channel_summary.sort_values("ctr", ascending=True)

    fig, ax = plt.subplots(figsize=(STYLE["chart_width"], STYLE["chart_height"]))
    colors = _get_colors(len(df))
    ax.barh(df["channel"], df["ctr"], color=colors, edgecolor="white", height=0.6)

    for bar, val in zip(ax.patches, df["ctr"]):
        ax.text(bar.get_width() + df["ctr"].max() * 0.02,
                bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%", va="center", fontsize=STYLE["tick_fontsize"])

    ax.set_title("各渠道点击率(CTR)对比", fontsize=STYLE["title_fontsize"], fontweight="bold")
    ax.set_xlabel("CTR (%)", fontsize=STYLE["label_fontsize"])
    ax.grid(True, axis="x", alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=STYLE["dpi"], bbox_inches="tight")
    plt.close(fig)
    return save_path


def plot_weekly_trend(weekly_df, save_path=None):
    """绘制周度GMV趋势图（分渠道）

    Args:
        weekly_df: 周度对比数据
        save_path: 保存路径
    """
    fig, ax = plt.subplots(figsize=(STYLE["chart_width"], STYLE["chart_height"]))

    channels = weekly_df["channel"].unique()
    colors = _get_colors(len(channels))

    for ch, color in zip(channels, colors):
        sub = weekly_df[weekly_df["channel"] == ch].sort_values("year_week")
        ax.plot(sub["year_week"], sub["weekly_gmv"],
                marker="o", linewidth=2, label=ch, color=color)

    ax.set_title("周度GMV趋势（分渠道）", fontsize=STYLE["title_fontsize"], fontweight="bold")
    ax.set_xlabel("周次", fontsize=STYLE["label_fontsize"])
    ax.set_ylabel("周GMV", fontsize=STYLE["label_fontsize"])
    ax.legend(loc="upper right", fontsize=STYLE["tick_fontsize"])
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=STYLE["dpi"], bbox_inches="tight")
    plt.close(fig)
    return save_path


def plot_cost_gmv_scatter(channel_summary, save_path=None):
    """绘制花费-GMV散点图

    Args:
        channel_summary: 渠道汇总表（含total_cost和total_gmv列）
        save_path: 保存路径
    """
    fig, ax = plt.subplots(figsize=(STYLE["chart_width"], STYLE["chart_height"]))

    colors = _get_colors(len(channel_summary))
    for i, row in channel_summary.iterrows():
        ax.scatter(row["total_cost"], row["total_gmv"],
                   s=200, color=colors[i], label=row["channel"],
                   edgecolors="white", linewidth=2, zorder=5)

    # 添加ROI趋势线
    z = np.polyfit(channel_summary["total_cost"], channel_summary["total_gmv"], 1)
    p = np.poly1d(z)
    x_line = np.linspace(channel_summary["total_cost"].min(),
                         channel_summary["total_cost"].max(), 100)
    ax.plot(x_line, p(x_line), "--", alpha=0.5, color="gray", label="趋势线")

    ax.set_title("花费 vs GMV 散点图", fontsize=STYLE["title_fontsize"], fontweight="bold")
    ax.set_xlabel("总花费", fontsize=STYLE["label_fontsize"])
    ax.set_ylabel("总GMV", fontsize=STYLE["label_fontsize"])
    ax.legend(loc="upper left", fontsize=STYLE["tick_fontsize"])
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=STYLE["dpi"], bbox_inches="tight")
    plt.close(fig)
    return save_path


def generate_all_charts(daily_df, channel_summary, weekly_df, charts_dir):
    """批量生成所有图表

    Args:
        daily_df: 日趋势数据
        channel_summary: 渠道汇总表
        weekly_df: 周度数据
        charts_dir: 图表保存目录
    """
    os.makedirs(charts_dir, exist_ok=True)

    charts = [
        ("daily_gmv_trend.png", plot_daily_gmv_trend(daily_df,
                                                     os.path.join(charts_dir, "daily_gmv_trend.png"))),
        ("channel_gmv_comparison.png", plot_channel_comparison(channel_summary,
                                                               os.path.join(charts_dir, "channel_gmv_comparison.png"))),
        ("channel_ctr.png", plot_channel_ctr_bar(channel_summary,
                                                 os.path.join(charts_dir, "channel_ctr.png"))),
        ("weekly_trend.png", plot_weekly_trend(weekly_df,
                                               os.path.join(charts_dir, "weekly_trend.png"))),
        ("cost_gmv_scatter.png", plot_cost_gmv_scatter(channel_summary,
                                                       os.path.join(charts_dir, "cost_gmv_scatter.png"))),
    ]

    generated = [c[0] for c in charts if c[1] is not None]
    print(f"成功生成 {len(generated)} 张图表: {generated}")
    return generated