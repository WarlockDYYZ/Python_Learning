from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.mysql import insert
from Stage_Three.Python.Day9.app.models.behavior import UserBehavior
from Stage_Three.Python.Day9.app.schemas.behavior import BehaviorCreate
from typing import List
from loguru import logger


class BulkLoader:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.batch_size = 1000  # 每批次入库数据量

    async def bulk_insert_behavior(self, data: List[BehaviorCreate]) -> int:
        """批量插入用户行为数据，返回成功入库的条数"""
        if not data:
            return 0

        # 转换为数据库字典列表，过滤模型中多余的字段
        insert_data = [item.model_dump(exclude_unset=True) for item in data]

        try:
            # 采用SQLAlchemy Core的批量插入方式，性能远高于ORM单条插入
            stmt = insert(UserBehavior).values(insert_data)
            result = await self.db.execute(stmt)
            await self.db.commit()
            logger.info(f"成功批量插入{result.rowcount}条行为数据")
            return result.rowcount
        except Exception as e:
            await self.db.rollback()
            logger.error(f"批量插入行为数据失败：{str(e)}")
            raise

    async def upsert_behavior(self, data: List[BehaviorCreate]) -> int:
        """增量写入：如果主键冲突或唯一索引冲突则执行更新逻辑，支持断点续传"""
        if not data:
            return 0

        insert_data = [item.model_dump(exclude_unset=True) for item in data]
        # MySQL特有语法：ON DUPLICATE KEY UPDATE，配置冲突后需更新的字段
        stmt = insert(UserBehavior).values(insert_data)
        stmt = stmt.on_duplicate_key_update(
            action_type=stmt.inserted.action_type,
            target_id=stmt.inserted.target_id,
            metadata=stmt.inserted.metadata,
            ip_address=stmt.inserted.ip_address,
            user_agent=stmt.inserted.user_agent
        )

        try:
            result = await self.db.execute(stmt)
            await self.db.commit()
            logger.info(f"成功增量更新{result.rowcount}条行为数据")
            return result.rowcount
        except Exception as e:
            await self.db.rollback()
            logger.error(f"增量更新行为数据失败：{str(e)}")
            raise