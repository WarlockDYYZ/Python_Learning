"""D5: 业务洞察模块

从数据中提炼业务结论，生成结构化分析报告。
采用"数据 -> 洞察 -> 建议"的叙事结构。
"""
import pandas as pd
import numpy as np


def generate_insights(channel_summary, weekly_df, anomalies, daily_df):
    """生成业务洞察文本

    Args:
        channel_summary: 渠道汇总表
        weekly_df: 周度对比数据
        anomalies: 异常检测记录
        daily_df: 日趋势数据

    Returns:
        洞察报告文本
    """
    lines = []
    lines.append("# 多渠道运营数据分析报告\n")
    lines.append("## 一、整体概览\n")

    # 整体数据
    total_gmv = channel_summary["total_gmv"].sum()
    total_clicks = channel_summary["total_clicks"].sum()
    total_cost = channel_summary["total_cost"].sum()
    total_users = channel_summary["total_new_users"].sum()

    lines.append(f"- 分析期间总GMV: **{total_gmv:,.0f}**")
    lines.append(f"- 总点击量: **{total_clicks:,}**")
    lines.append(f"- 总花费: **{total_cost:,.0f}**")
    lines.append(f"- 新增用户: **{total_users:,}**")
    lines.append(f"- 整体CTR: **{channel_summary['ctr'].mean():.1f}%**")
    lines.append(f"- 整体CPC: **{channel_summary['cpc'].mean():.2f}**\n")

    # 渠道排名
    lines.append("## 二、渠道表现排名\n")
    lines.append("按GMV排序:\n")
    lines.append("| 排名 | 渠道 | GMV | 占比 |")
    lines.append("|------|------|-----|------|")
    for i, row in channel_summary.sort_values("total_gmv", ascending=False).iterrows():
        pct = row["total_gmv"] / total_gmv * 100
        lines.append(f"| {i + 1} | {row['channel']} | {row['total_gmv']:,.0f} | {pct:.1f}% |")
    lines.append("")

    # 最佳渠道
    best_channel = channel_summary.loc[channel_summary["total_gmv"].idxmax()]
    lines.append(f"**表现最佳渠道**: {best_channel['channel']}，GMV达 {best_channel['total_gmv']:,.0f}，"
                 f"占总体 {best_channel['total_gmv'] / total_gmv * 100:.1f}%。"
                 f"该渠道CTR为 {best_channel['ctr']:.1f}%，CPC为 {best_channel['cpc']:.2f}。\n")

    # 周度趋势
    if len(weekly_df) > 0:
        lines.append("## 三、周度趋势分析\n")
        recent_weeks = weekly_df.sort_values("year_week").tail(3)
        for _, wrow in recent_weeks.iterrows():
            woq = f"{wrow.get('gmv_woq', 0):+.1f}%" if pd.notna(wrow.get('gmv_woq', None)) else "N/A"
            lines.append(f"- {wrow['year_week']}: GMV={wrow['weekly_gmv']:,.0f}，环比 {woq}")
        lines.append("")

    # 异常检测
    if len(anomalies) > 0:
        lines.append("## 四、异常数据预警\n")
        lines.append(f"共检测到 **{len(anomalies)}** 条异常记录:\n")
        for _, arow in anomalies.iterrows():
            lines.append(f"- {arow.get('date', '?')} | {arow.get('channel', '?')} | "
                         f"GMV={arow.get('gmv', '?')} | 方法={arow.get('rule', '?')} | "
                         f"偏离度={arow.get('deviation', '?'):.1f}x")
        lines.append("")

    # 建议
    lines.append("## 五、业务建议\n")

    # 基于数据的建议
    best_gmv_ch = channel_summary.loc[channel_summary["total_gmv"].idxmax()]
    worst_gmv_ch = channel_summary.loc[channel_summary["total_gmv"].idxmin()]

    lines.append(f"1. **加大优质渠道投入**: {best_gmv_ch['channel']}表现最优，建议适当增加预算分配，"
                 f"预计可带来 {best_gmv_ch['total_gmv'] / total_gmv * 100:.0f}% 的GMV贡献。")

    lines.append(f"2. **优化低效渠道**: {worst_gmv_ch['channel']}贡献最低，建议审查投放策略，"
                 f"考虑优化素材或调整出价策略。")

    if len(anomalies) > 0:
        lines.append(f"3. **排查异常数据**: 检测到 {len(anomalies)} 条异常记录，建议人工核实是否为真实业务波动"
                     f"还是数据采集异常，避免误判影响决策。")

    lines.append("4. **持续监控**: 建议建立每日自动化监控流程，设置阈值告警，及时发现异常波动。")

    return "\n".join(lines)