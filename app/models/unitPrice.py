from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class UnitPrice(Base):
    __tablename__ = "unitPrice"  # نام جدول

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Integer, nullable=False, index=True, unique=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="unitPrice")


from app.models.user import User
