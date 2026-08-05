from datetime import datetime
from typing import List, Dict
from Stage_Three.Python.Day9.app.schemas.behavior import BehaviorCreate
from loguru import logger
import re


def clean_behavior_data(raw_data: List[Dict]) -> List[BehaviorCreate]:
    """清洗用户行为原始数据，返回校验后的Pydantic模型列表"""
    cleaned = []
    for idx, item in enumerate(raw_data):
        try:
            # 1. 脱敏敏感数据：移除IP地址最后一段，脱敏用户UA中的隐私信息
            if item.get("ip_address"):
                item["ip_address"] = re.sub(r"\.\d+$", ".0", item["ip_address"])
            # 2. 过滤无效行为类型：仅保留系统预设的行为类型
            if item["action_type"] not in ["view", "click", "search", "share", "like"]:
                logger.warning(f"第{idx}条数据存在非法行为类型：{item['action_type']}，跳过")
                continue
            # 3. 校验必填字段：user_id、action_type不能为空
            if not item.get("user_id") or not item.get("action_type"):
                logger.warning(f"第{idx}条数据缺少必填字段，跳过")
                continue
            # 4. 统一时间格式：将不同源的时间戳转为MySQL兼容的datetime格式
            if isinstance(item.get("created_at"), int):
                item["created_at"] = datetime.fromtimestamp(item["created_at"]).strftime("%Y-%m-%d %H:%M:%S")
            # 5. 用Pydantic模型校验数据格式
            cleaned.append(BehaviorCreate(**item))
        except Exception as e:
            logger.error(f"清洗第{idx}条数据失败：{str(e)}，原始数据：{item}")
            continue
    return cleaned