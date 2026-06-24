# app/crud/product.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.product import Product
from app.schemas.product import ProductCreate


async def get_product_by_id(db: AsyncSession, product_id: int) -> Product:
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
    category: str | None = None
) -> list[Product]:
    """异步分页查询商品列表，支持分类筛选"""
    # 构建基础查询语句
    query = select(Product).offset(skip).limit(limit).order_by(Product.created_at.desc())
    # 动态添加分类筛选条件
    if category:
        query = query.where(Product.category == category)
    # 异步执行查询
    result = await db.execute(query)
    return result.scalars().all()