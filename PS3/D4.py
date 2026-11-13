import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.db_storage import fetch_source, save_records, init_db
from app.query_service import QueryService
from app.exporter import report_upstream

logger = logging.getLogger(__name__)


def daily_etl_job():
    """
    每日 ETL 任务：抽取 T-1 增量数据，落库后汇总并上报。
    """
    start_time = datetime.now()
    target_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    try:
        init_db()
        rows = fetch_source(start=target_date, end=target_date)

        saved = save_records(rows)

        summary = QueryService().summarize()

        payload = {
            "saved": saved,
            "total_gmv": summary.get("total_gmv", 0.0),
            "total_orders": summary.get("total_orders", 0),
            "by_channel": summary.get("by_channel", [])
        }
        code = report_upstream(payload)

        cost_sec = round((datetime.now() - start_time).total_seconds(), 2)
        logger.info(
            "[ETL完成] date=%s saved=%s total_gmv=%s report_code=%s cost=%ss",
            target_date, saved, payload["total_gmv"], code, cost_sec
        )
        return saved

    except Exception as e:
        cost_sec = round((datetime.now() - start_time).total_seconds(), 2)
        # 记录完整堆栈，并附带耗时和日期信息，方便排查
        logger.exception("[ETL失败] date=%s cost=%ss error=%s", target_date, cost_sec, e)
        return None


def build_scheduler():
    """
    构建后台调度器，配置持久化与防并发。
    """
    sched = BackgroundScheduler(timezone="Asia/Shanghai")

    # - id: 唯一标识，配合 replace_existing=True 防止重启时重复注册
    # - coalesce=True: 如果错过了多次触发（如服务宕机重启），合并为一次执行
    # - max_instances=1: 严格防并发，上一次没跑完绝不启动下一次
    # - misfire_grace_time: 允许 1 小时的错过容忍度
    sched.add_job(
        daily_etl_job,
        CronTrigger(hour=2, minute=0),
        id="daily_etl",
        replace_existing=True,
        coalesce=True,
        max_instances=1,
        misfire_grace_time=3600
    )

    logger.info("ETL调度器构建完成，将于每日 02:00 (Asia/Shanghai) 执行")
    return sched