import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.db_storage import fetch_source, save_records, init_db
from app.query_service import QueryService
from app.exporter import report_upstream

logger = logging.getLogger(__name__)


def daily_etl_job():
    try:
        init_db()
        rows = fetch_source()
        saved = save_records(rows)
        summary = QueryService().summarize()
        code = report_upstream({"saved": saved, **{k: summary[k] for k in summary}})
        logger.info("[ETL完成] saved=%s total_gmv=%s report_code=%s",
                    saved, summary["total_gmv"], code)
        return saved
    except Exception as e:
        logger.exception("[ETL失败] %s", e)
        return None


def build_scheduler():
    sched = BackgroundScheduler(timezone="Asia/Shanghai")
    # 每天 02:00 跑增量；interval 触发器适合"每 N 分钟"场景
    sched.add_job(daily_etl_job, CronTrigger(hour=2, minute=0), id="daily_etl",
                  replace_existing=True)
    return sched