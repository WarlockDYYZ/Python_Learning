# app/etl/api_client.py
from asyncio.log import logger

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, before_sleep_log, asyncio
from typing import Dict, Optional, List
from Stage_Three.Python.Day9.app.config import settings
import hashlib
import time
import logging


# 创建一个专属的官方 logger
logger = logging.getLogger(__name__)
before_sleep=before_sleep_log(logger, logging.WARNING)

class ETLApiClient:
    def __init__(self, base_url: str, ak: str, sk: str):
        """
        API抽取客户端
        :param base_url: 接口基础地址
        :param ak: 接口访问凭证AccessKey
        :param sk: 接口访问密钥SecretKey
        """
        self.base_url = base_url.rstrip("/")
        self.ak = ak
        self.sk = sk
        self.client = httpx.AsyncClient(timeout=30.0)  # 统一30秒超时

    def _generate_signature(self, params: Dict) -> str:
        """生成接口签名（根据第三方文档规则实现，此处为RSA2示例）"""
        sorted_params = sorted(params.items(), key=lambda x: x[0])
        sign_str = "&".join([f"{k}={v}" for k, v in sorted_params])
        sign_str += f"&sk={self.sk}"
        return hashlib.sha256(sign_str.encode()).hexdigest()

    @retry(
        stop=stop_after_attempt(3),  # 最多重试3次
        wait=wait_exponential(multiplier=1, min=2, max=10),  # 指数退避等待
        retry=retry_if_exception_type((httpx.NetworkError, httpx.TimeoutException)),
        before_sleep = before_sleep_log(logger, logging.WARNING)  # 新增：重试前打印警告日志
    )
    async def request(self, method: str, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """通用请求方法，自动添加鉴权参数、处理重试逻辑"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        params = params or {}
        # 公共参数
        params["ak"] = self.ak
        params["timestamp"] = str(int(time.time()))
        params["sign"] = self._generate_signature(params)

        response = await self.client.request(method, url, params=params)
        response.raise_for_status()  # 抛出HTTP状态码异常
        return response.json()

    async def fetch_paginated_data(self, endpoint: str, page_size: int = 500) -> List[Dict]:
        """分页拉取API数据，适配大规模行为数据抽取"""
        all_data = []
        page = 1
        while True:
            resp = await self.request("GET", endpoint, params={"page": page, "page_size": page_size})
            if not resp["data"]: break
            yield resp["data"]  # 每次只吐出一页数据，边拉取边写入数据库
            await asyncio.sleep(0.1)
            page += 1

    async def close(self):
        """关闭HTTP客户端"""
        await self.client.aclose()