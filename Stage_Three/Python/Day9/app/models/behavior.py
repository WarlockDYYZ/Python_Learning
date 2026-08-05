from datetime import datetime

from sqlalchemy import Column, BigInteger, Integer, String, DateTime, JSON, ForeignKey, Index
from sqlalchemy.orm import relationship

from Stage_Three.Python.Day9.app.database import Base


class UserBehavior(Base):
    __tablename__ = "user_behaviors"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    action_type = Column(String(30), nullable=False, index=True)
    target_id = Column(String(100), default=None)
    metadata = Column(JSON, default=None)
    ip_address = Column(String(45), default=None)
    user_agent = Column(String(500), default=None)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # 与用户表的多对一关系
    user = relationship("User", back_populates="behaviors")

    __table_args__ = (
        Index("idx_user_action_created", "user_id", "action_type", "created_at"),
    )

    def __repr__(self):
        return f"<UserBehavior(id={self.id}, user_id={self.user_id}, action='{self.action_type}')>"