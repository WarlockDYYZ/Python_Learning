from sqlalchemy import BigInteger, Column, DateTime, Index, String
from sqlalchemy.sql import func
from app.models.database import Base


class UrlMapping(Base):
    __tablename__ = "url_mappings"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    short_code = Column(String(10), unique=True, nullable=False, index=True)
    original_url = Column(String(2048), nullable=False)
    created_at = Column(DateTime, default=func.utcnow(), nullable=False)
    expires_at = Column(DateTime, nullable=True)
    click_count = Column(BigInteger, default=0, nullable=False)

    __table_args__ = (
    Index("idx_short_code", "short_code"),
    )

def __repr__(self):
    return f"<UrlMapping(id={self.id}, short_code='{self.short_code}')>"
