"""主程序：一键运行完整数据分析流水线

用法:
    python main.py                          # 使用默认参数运行
    python main.py --start 2025-09-01 --end 2025-12-31  # 指定日期范围
    python main.py --channels 抖音 淘宝      # 指定渠道
    python main.py --output-dir ./my_output  # 指定输出目录
"""
import os
import sys
import argparse
import logging
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from src.generate_data import generate_sales_data
from src.clean import clean_sales_data
from src.filters import filter_df
from src.metrics import calc_channel_summary, calc_weekly_comparison, calc_daily_trend
from src.charts import generate_all_charts
from src.anomaly import detect_anomalies, load_rules
from src.exporter import export_report_excel
from src.insight import generate_insights

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


def parse_args():
    parser = argparse.ArgumentParser(description="多渠道运营数据分析系统")
    parser.add_argument("--start", type=str, default="2025-09-01", help="起始日期")
    parser.add_argument("--end", type=str, default="2025-12-31", help="结束日期")
    parser.add_argument("--channels", nargs="+", type=str, default=None, help="渠道列表")
    parser.add_argument("--output-dir", type=str, default="output", help="输出目录")
    parser.add_argument("--generate-data", action="store_true", help="重新生成模拟数据")
    return parser.parse_args()


def main():
    args = parse_args()

    logger.info("=" * 60)
    logger.info("多渠道运营数据分析系统 启动")
    logger.info(f"参数: start={args.start}, end={args.end}, channels={args.channels}")

    # 确保输出目录存在
    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs("output/charts", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    # Step 1: 生成/加载数据
    logger.info("[Step 1] 准备数据")
    data_path = "data/raw/sales_daily.csv"

    if args.generate_data or not os.path.exists(data_path):
        logger.info("生成模拟数据...")
        df_raw = generate_sales_data()
        df_raw.to_csv(data_path, index=False, encoding="utf-8-sig")
        logger.info(f"数据已保存: {data_path}")
    else:
        logger.info(f"从文件加载数据: {data_path}")

    # Step 2: 数据清洗
    logger.info("[Step 2] 数据清洗")
    import pandas as pd
    df_raw = pd.read_csv(data_path)
    df_clean = clean_sales_data(df_raw)

    # Step 3: 数据筛选
    logger.info("[Step 3] 数据筛选")
    df_filtered = filter_df(
        df_clean,
        start_date=args.start,
        end_date=args.end,
        channels=args.channels
    )
    logger.info(f"筛选后数据: {len(df_filtered)} 行")

    # Step 4: 指标计算
    logger.info("[Step 4] 指标计算")
    channel_summary = calc_channel_summary(df_filtered)
    weekly_df = calc_weekly_comparison(df_filtered)
    daily_df = calc_daily_trend(df_filtered)
    logger.info(f"渠道汇总:\n{channel_summary.to_string()}")

    # Step 5: 可视化图表
    logger.info("[Step 5] 生成可视化图表")
    charts_dir = "output/charts"
    chart_files = generate_all_charts(daily_df, channel_summary, weekly_df, charts_dir)
    logger.info(f"生成图表: {chart_files}")

    # Step 6: 异常检测
    logger.info("[Step 6] 异常检测")
    anomalies = detect_anomalies(df_filtered)
    if len(anomalies) > 0:
        logger.warning(f"检测到 {len(anomalies)} 条异常记录")
        logger.info(f"异常记录:\n{anomalies.to_string()}")

    # Step 7: 导出报表
    logger.info("[Step 7] 导出Excel报表")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"report_{timestamp}.xlsx"
    report_path = os.path.join(args.output_dir, report_filename)
    export_report_excel(df_filtered, channel_summary, weekly_df, anomalies, charts_dir, report_path)

    # Step 8: 生成洞察文档
    logger.info("[Step 8] 生成业务洞察")
    insights = generate_insights(channel_summary, weekly_df, anomalies, daily_df)
    insights_path = os.path.join(args.output_dir, "insight_report.md")
    with open(insights_path, "w", encoding="utf-8") as f:
        f.write(insights)
    logger.info(f"洞察报告已保存: {insights_path}")

    logger.info("=" * 60)
    logger.info("分析流水线执行完成!")
    logger.info(f"报表路径: {report_path}")
    logger.info(f"洞察报告: {insights_path}")
    logger.info(f"图表目录: {charts_dir}")

    return report_path, insights_path


if __name__ == "__main__":
    report_path, insights_path = main()