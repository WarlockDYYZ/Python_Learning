import asyncio
import argparse
from loguru import logger
from Stage_Three.Python.Day9.app.etl.extract.db_extract import extract_behavior_from_db
from Stage_Three.Python.Day9.app.etl.extract.api_extract import extract_user_behavior_from_api
from Stage_Three.Python.Day9.app.etl.transform.cleaner import clean_behavior_data
from Stage_Three.Python.Day9.app.etl.load.bulk_loader import BulkLoader
from Stage_Three.Python.Day9.app.etl.db_pool import get_async_session
from Stage_Three.Python.Day9.app.utils.alarm import send_wechat_alarm  # 企业微信告警工具


async def full_sync():
    """全量同步历史行为数据，首次上线时执行"""
    try:
        logger.info("开始全量同步用户行为数据")
        # 1. 从业务MySQL抽取历史数据
        raw_db_data = await extract_behavior_from_db(start_time="2024-01-01", end_time="2024-12-31")
        # 2. 从API抽取补充行为数据
        raw_api_data = await extract_user_behavior_from_api(start_time="2024-01-01", end_time="2024-12-31")
        # 3. 合并多源数据并清洗
        cleaned_data = clean_behavior_data(raw_db_data + raw_api_data)
        # 4. 批量入库
        async with get_async_session("target_mysql") as db:
            loader = BulkLoader(db)
            await loader.bulk_insert_behavior(cleaned_data)
        logger.info("全量同步用户行为数据完成")
    except Exception as e:
        logger.error(f"全量同步失败：{str(e)}")
        await send_wechat_alarm("ETL全量同步任务失败", str(e))
        raise

async def incr_sync(start_time: str, end_time: str):
    """增量同步指定时间范围内的行为数据，可按小时/天定时调度"""
    try:
        logger.info(f"开始增量同步用户行为数据：{start_time} ~ {end_time}")
        # 1. 从API抽取增量数据
        raw_api_data = await extract_user_behavior_from_api(start_time, end_time)
        # 2. 清洗增量数据
        cleaned_data = clean_behavior_data(raw_api_data)
        # 3. 增量入库（冲突时更新）
        async with get_async_session("target_mysql") as db:
            loader = BulkLoader(db)
            await loader.upsert_behavior(cleaned_data)
        logger.info(f"增量同步用户行为数据完成：{start_time} ~ {end_time}")
    except Exception as e:
        logger.error(f"增量同步失败：{str(e)}")
        await send_wechat_alarm("ETL增量同步任务失败", str(e))
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="用户行为数据ETL同步工具")
    parser.add_argument("--mode", required=True, choices=["full", "incr"], help="同步模式：full=全量同步，incr=增量同步")
    parser.add_argument("--start-time", help="增量同步开始时间，格式为YYYY-MM-DD HH:MM:SS")
    parser.add_argument("--end-time", help="增量同步结束时间，格式为YYYY-MM-DD HH:MM:SS")
    args = parser.parse_args()

    if args.mode == "full":
        asyncio.run(full_sync())
    elif args.mode == "incr":
        if not args.start_time or not args.end_time:
            raise ValueError("增量同步必须指定--start-time和--end-time参数")
        asyncio.run(incr_sync(args.start_time, args.end_time))