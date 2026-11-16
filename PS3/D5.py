import os, csv, logging, requests
from datetime import datetime
from app.config import OUT_DIR, REPORT_URL

logger = logging.getLogger(__name__)


def export_excel(rows, filename="report.xlsx"):
    # 1. 空数据防御：避免 rows[0] 抛出 IndexError
    if not rows:
        logger.warning("无数据可导出，跳过 Excel: %s", filename)
        return None

    # 延迟导入，避免未安装 openpyxl 时拖慢启动
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill

    # 2. 自动创建输出目录
    os.makedirs(OUT_DIR, exist_ok=True)

    # 3. 文件名日期化，防止每日覆盖
    date_str = datetime.now().strftime("%Y%m%d")
    name, ext = os.path.splitext(filename)
    path = os.path.join(OUT_DIR, f"{name}_{date_str}{ext}")

    wb = Workbook()
    ws = wb.active
    ws.title = "sales"

    headers = list(rows[0].keys())
    ws.append(headers)

    # 表头样式
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="2E7D32")

    # 写入数据行
    for r in rows:
        ws.append([r.get(h) for h in headers])  # 使用 get 防止某行缺键导致崩溃

    # 4. 自适应列宽：修复 None 转 'None' 和 datetime 过长的问题
    for col in ws.columns:
        max_length = 0
        for c in col:
            val = c.value
            # 处理 None 和 datetime 对象
            if val is None:
                str_val = ""
            elif isinstance(val, datetime):
                str_val = val.strftime("%Y-%m-%d")
            else:
                str_val = str(val)
            max_length = max(max_length, len(str_val))
        ws.column_dimensions[col[0].column_letter].width = max_length + 2

    wb.save(path)
    logger.info("Excel 导出完成: %s", path)
    return path


def export_csv(rows, filename="report.csv"):
    # 1. 空数据防御
    if not rows:
        logger.warning("无数据可导出，跳过 CSV: %s", filename)
        return None

    # 2. 自动创建输出目录
    os.makedirs(OUT_DIR, exist_ok=True)

    # 3. 文件名日期化
    date_str = datetime.now().strftime("%Y%m%d")
    name, ext = os.path.splitext(filename)
    path = os.path.join(OUT_DIR, f"{name}_{date_str}{ext}")

    # 4. 收集所有行的键并集，防止 DictWriter 遇到多余键报错
    all_keys = list(dict.fromkeys(k for r in rows for k in r.keys()))

    # 8. CSV 公式注入防护：过滤以危险字符开头的值
    def sanitize_value(val):
        if isinstance(val, str) and val.startswith(('=', '+', '-', '@')):
            return "'" + val
        return val

    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=all_keys, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: sanitize_value(v) for k, v in r.items()})

    logger.info("CSV 导出完成: %s", path)
    return path


def report_upstream(payload, session=None):
    """上报到下游。对网络异常、序列化异常做兜底，保证主流程不被拖垮。"""
    sess = session or requests
    try:
        resp = sess.post(REPORT_URL, json=payload, timeout=5)

        # 7. 校验 HTTP 状态码
        if resp.status_code >= 400:
            logger.warning("上报被拒 status=%s body=%s", resp.status_code, resp.text[:200])
        else:
            logger.info("上报完成 status=%s", resp.status_code)

        return resp.status_code

    # 6. 扩大异常捕获范围：防止 payload 含 NaN/Numpy 类型导致序列化失败时任务崩溃
    except (requests.RequestException, TypeError, ValueError) as e:
        logger.warning("上报失败(已降级): %s", e)
        return None