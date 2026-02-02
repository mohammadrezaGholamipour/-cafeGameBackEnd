from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

class UnitPrice(Base):
    __tablename__ = "unitPrice"

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Integer, nullable=False, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="unitPrice")

    __table_args__ = (
        UniqueConstraint("owner_id", "price", name="uq_owner_price"),
    )



from app.models.user import User
