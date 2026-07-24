# app/crud/product.py
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import Product
from app import ProductCreate


async def get_product_by_id(db: AsyncSession, product_id: int) -> Optional[Product]:
    """根据ID异步查询商品详情"""
    # 异步执行SELECT查询，await挂起，等待数据库I/O完成
    result = await db.execute(select(Product).where(Product.id == product_id))
    # 获取单条查询结果
    return result.scalar_one_or_none()

async def create_product(db: AsyncSession, product: ProductCreate) -> Product:
    """异步创建商品记录"""
    db_product = Product(**product.model_dump())
    db.add(db_product)
    # 异步刷新事务，获取数据库生成的自增ID
    await db.flush()
    await db.refresh(db_product)
    return db_product

async def get_products_paginated(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None
) -> List[Product]:
    """异步分页查询商品列表，支持分类筛选"""
    stmt = select(Product).offset(skip).limit(limit).order_by(Product.created_at.desc())
    filter_conditions = []
    # 条件放入列表，不链式拼接where
    if category:
        filter_conditions.append(Product.category == category)
    # 一次性拼接所有条件
    if filter_conditions:
        stmt = stmt.where(*filter_conditions)
    result = await db.execute(stmt)
    return list(result.scalars().all())