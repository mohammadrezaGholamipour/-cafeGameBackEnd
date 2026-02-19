from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base


class Bill(Base):
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    console_id = Column(Integer, ForeignKey("consoles.id"), nullable=False)
    unit_price_amount = Column(Integer, nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=True)
    play_price = Column(Integer, nullable=True, default=0)
    total_price = Column(Integer, nullable=True, default=0)
    payment_method = Column(Integer, nullable=True, default=0)
    owner = relationship("User", back_populates="bills")
    console = relationship("Console")
    bill_foods = relationship(
        "BillFood",
        back_populates="bill",
        cascade="all, delete-orphan"
    )


from app.models.billFood import BillFood