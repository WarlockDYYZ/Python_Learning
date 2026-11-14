import os, csv, logging, requests
from app.config import OUT_DIR, REPORT_URL

logger = logging.getLogger(__name__)


def export_excel(rows, filename="report.xlsx"):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill
    path = os.path.join(OUT_DIR, filename)
    wb = Workbook();
    ws = wb.active;
    ws.title = "sales"
    headers = list(rows[0].keys())
    ws.append(headers)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="2E7D32")
    for r in rows:
        ws.append([r[h] for h in headers])
    for col in ws.columns:  # 自适应列宽
        width = max(len(str(c.value)) for c in col) + 2
        ws.column_dimensions[col[0].column_letter].width = width
    wb.save(path)
    logger.info("Excel 导出完成: %s", path)
    return path


def export_csv(rows, filename="report.csv"):
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:  # utf-8-sig 防 Excel 乱码
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader();
        w.writerows(rows)
    logger.info("CSV 导出完成: %s", path)
    return path


def report_upstream(payload, session=None):
    """上报到下游。真实环境会带鉴权头；这里对网络异常做兜底，保证主流程不被拖垮。"""
    sess = session or requests
    try:
        resp = sess.post(REPORT_URL, json=payload, timeout=5)
        logger.info("上报完成 status=%s", resp.status_code)
        return resp.status_code
    except requests.RequestException as e:  # 外网不可达时降级
        logger.warning("上报失败(已降级): %s", e)
        return None