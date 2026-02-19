from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class BillFood(Base):
    __tablename__ = "bill_foods"

    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(Integer, ForeignKey("bills.id"), nullable=False)
    food_id = Column(Integer, ForeignKey("buffet.id"), nullable=False)

    count = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    name = Column(String, nullable=False)

    bill = relationship("Bill", back_populates="bill_foods")



from app.models.buffet import Buffet
from app.models.bill import Bill
