from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base


class Bill(Base):
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    console_id = Column(Integer, ForeignKey("consoles.id"), nullable=False)
    unit_price_id = Column(Integer, ForeignKey("unitPrice.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    play_price = Column(Integer, nullable=True, default=0)
    total_price = Column(Integer, nullable=True, default=0)
    owner = relationship("User", back_populates="bills")
    console = relationship("Console")
    unit_price = relationship("UnitPrice")

