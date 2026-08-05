from Stage_Three.Python.Day9.app.etl.api_client import ETLApiClient
from Stage_Three.Python.Day9.app.config import settings
from typing import List, Dict

async def extract_user_behavior_from_api(start_time: str, end_time: str) -> List[Dict]:
    """从用户行为API抽取指定时间范围内的增量数据"""
    client = ETLApiClient(
        base_url=settings.BEHAVIOR_API_BASE,
        ak=settings.ETL_API_AK,
        sk=settings.ETL_API_SK
    )
    try:
        behavior_data = await client.fetch_paginated_data(
            endpoint="/api/v1/behaviors/export",
            params={"start_time": start_time, "end_time": end_time}
        )
        return behavior_data
    finally:
        await client.close()