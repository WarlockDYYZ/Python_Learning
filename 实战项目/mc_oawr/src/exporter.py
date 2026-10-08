"""D5: 报表导出模块

使用openpyxl生成格式化的Excel报表，包含：
- 汇总表（各渠道核心指标）
- 分渠道明细表
- 异常检测清单
- 条件格式（红字标跌幅>20%）
"""
import os
from datetime import datetime
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, numbers
from openpyxl.utils import get_column_letter


def export_report_excel(df, channel_summary, weekly_df, anomalies, charts_dir, output_path):
    """导出完整分析报表到Excel

    Args:
        df: 筛选后的原始数据
        channel_summary: 渠道汇总表
        weekly_df: 周度对比数据
        anomalies: 异常检测记录
        charts_dir: 图表目录路径
        output_path: 输出文件路径
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    wb = Workbook()

    # ===== Sheet1: 汇总概览 =====
    ws1 = wb.active
    ws1.title = "汇总概览"

    # 标题行
    ws1.merge_cells("A1:G1")
    title_cell = ws1["A1"]
    title_cell.value = f"多渠道运营数据分析周报 ({df['date'].min().strftime('%Y-%m-%d')} ~ {df['date'].max().strftime('%Y-%m-%d')})"
    title_cell.font = Font(name="微软雅黑", size=14, bold=True, color="FFFFFF")
    title_cell.fill = PatternFill(start_color="2E86AB", end_color="2E86AB", fill_type="solid")
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws1.row_dimensions[1].height = 35

    # 表头
    headers = ["渠道", "总GMV", "总曝光", "总点击", "总花费", "新增用户", "CTR(%)", "CPC", "日均GMV"]
    for col, header in enumerate(headers, 1):
        cell = ws1.cell(row=3, column=col, value=header)
        cell.font = Font(name="微软雅黑", size=11, bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="A23B72", end_color="A23B72", fill_type="solid")
        cell.alignment = Alignment(horizontal="center", vertical="center")

    # 数据行
    thin_border = Border(
        left=Side(style="thin"), right=Side(style="thin"),
        top=Side(style="thin"), bottom=Side(style="thin")
    )

    for i, row in channel_summary.iterrows():
        r = i + 4
        values = [
            row["channel"],
            row["total_gmv"],
            row["total_exposure"],
            row["total_clicks"],
            row["total_cost"],
            row["total_new_users"],
            row["ctr"],
            row["cpc"],
            row["avg_daily_gmv"],
        ]
        for col, val in enumerate(values, 1):
            cell = ws1.cell(row=r, column=col, value=val)
            cell.font = Font(name="微软雅黑", size=10)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal="center" if col > 1 else "left")

            # 数值格式
            if col in [2, 5]:  # GMV、花费
                cell.number_format = '#,##0.00'
            elif col in [3, 4, 6]:  # 整数
                cell.number_format = '#,##0'
            elif col in [7]:  # CTR
                cell.number_format = '0.0'
            elif col in [8, 9]:  # CPC、日均GMV
                cell.number_format = '0.00'

    # 设置列宽
    col_widths = [12, 15, 12, 12, 12, 12, 10, 10, 12]
    for i, w in enumerate(col_widths, 1):
        ws1.column_dimensions[get_column_letter(i)].width = w

    # ===== Sheet2: 周度趋势 =====
    if len(weekly_df) > 0:
        ws2 = wb.create_sheet("周度趋势")
        ws2.merge_cells("A1:D1")
        title2 = ws2["A1"]
        title2.value = "周度GMV趋势"
        title2.font = Font(name="微软雅黑", size=12, bold=True)
        title2.alignment = Alignment(horizontal="center")

        weekly_headers = ["周次", "渠道", "周GMV", "环比变化(%)"]
        for col, header in enumerate(weekly_headers, 1):
            cell = ws2.cell(row=3, column=col, value=header)
            cell.font = Font(name="微软雅黑", size=10, bold=True)
            cell.fill = PatternFill(start_color="F18F01", end_color="F18F01", fill_type="solid")
            cell.font = Font(name="微软雅黑", size=10, bold=True, color="FFFFFF")
            cell.alignment = Alignment(horizontal="center")

        for i, row in weekly_df.iterrows():
            r = i + 4
            woq_val = row.get("gmv_woq", None)
            if pd.notna(woq_val):
                woq_str = f"{woq_val:+.1f}%"
            else:
                woq_str = "-"

            values = [row["year_week"], row["channel"], row["weekly_gmv"], woq_str]
            for col, val in enumerate(values, 1):
                cell = ws2.cell(row=r, column=col, value=val)
                cell.font = Font(name="微软雅黑", size=10)
                cell.border = thin_border
                cell.alignment = Alignment(horizontal="center")

                # 条件格式：跌幅>20%标红
                if col == 4 and isinstance(val, str) and val.startswith("-"):
                    try:
                        pct = float(val.replace("%", "").replace("+", ""))
                        if pct < -20:
                            cell.font = Font(color="FF0000", bold=True)
                    except (ValueError, TypeError):
                        pass

    # ===== Sheet3: 异常检测清单 =====
    if len(anomalies) > 0:
        ws3 = wb.create_sheet("异常检测清单")
        ws3.merge_cells("A1:F1")
        title3 = ws3["A1"]
        title3.value = "异常数据检测清单"
        title3.font = Font(name="微软雅黑", size=12, bold=True)
        title3.alignment = Alignment(horizontal="center")

        anomaly_headers = ["日期", "渠道", "GMV", "检测方法", "偏离度", "备注"]
        for col, header in enumerate(anomaly_headers, 1):
            cell = ws3.cell(row=3, column=col, value=header)
            cell.font = Font(name="微软雅黑", size=10, bold=True)
            cell.fill = PatternFill(start_color="C73E1D", end_color="C73E1D", fill_type="solid")
            cell.font = Font(name="微软雅黑", size=10, bold=True, color="FFFFFF")
            cell.alignment = Alignment(horizontal="center")

        for i, row in anomalies.iterrows():
            r = i + 4
            values = [
                str(row.get("date", "")),
                row.get("channel", ""),
                row.get("gmv", ""),
                row.get("rule", ""),
                row.get("deviation", ""),
                "数值异常偏高"
            ]
            for col, val in enumerate(values, 1):
                cell = ws3.cell(row=r, column=col, value=val)
                cell.font = Font(name="微软雅黑", size=10)
                cell.border = thin_border
                cell.alignment = Alignment(horizontal="center")

    # ===== Sheet4: 图表目录 =====
    ws4 = wb.create_sheet("图表索引")
    ws4.merge_cells("A1:B1")
    ws4["A1"].value = "分析图表"
    ws4["A1"].font = Font(name="微软雅黑", size=12, bold=True)

    chart_files = [f for f in os.listdir(charts_dir) if f.endswith((".png", ".jpg"))] if os.path.exists(
        charts_dir) else []
    for i, chart_file in enumerate(chart_files):
        ws4.cell(row=i + 3, column=1, value=chart_file).font = Font(name="微软雅黑", size=10)
        chart_path = os.path.join(charts_dir, chart_file)
        if os.path.exists(chart_path):
            from openpyxl.drawing.image import Image as XLImage
            img = XLImage(chart_path)
            img.width = 600
            img.height = 300
            ws4.add_image(img, f"A{i + 5}")

    wb.save(output_path)
    print(f"报表已保存: {output_path}")
    return output_path