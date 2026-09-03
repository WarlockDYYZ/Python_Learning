import hashlib
from sqlalchemy import BigInteger, Column, DateTime, Index, Integer, String
from sqlalchemy.sql import func
from app.models.database import Base


class UrlMapping(Base):
    __tablename__ = "url_mappings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    short_code = Column(String(16), unique=True, nullable=False, index=True)
    original_url = Column(String(2048), nullable=False)
    created_at = Column(DateTime, default=func.utcnow(), nullable=False)
    url_hash = Column(String(64), unique=True, nullable=False, index=True)  # SHA-256 哈希索引
    expires_at = Column(DateTime, nullable=True)
    click_count = Column(BigInteger, default=0, nullable=False)

    @staticmethod
    def compute_url_hash(url: str) -> str:
        """对原始 URL 计算 SHA-256 哈希，用于快速查重"""
        return hashlib.sha256(url.encode("utf-8")).hexdigest()

    __table_args__ = (
        Index("idx_short_code", "short_code"),
    )


def __repr__(self):
    return f"<UrlMapping(id={self.id}, short_code='{self.short_code}')>"


'''
    数据库迁移：添加索引
    -- Alembic 迁移脚本
    ALTER TABLE url_mappings ADD COLUMN url_hash VARCHAR(64);

    -- 回填已有数据
    UPDATE url_mappings SET url_hash = SHA2(original_url, 256);

    -- 添加唯一索引（一个 URL 哈希只对应一条有效记录）
    ALTER TABLE url_mappings ADD UNIQUE INDEX idx_url_hash (url_hash);
'''