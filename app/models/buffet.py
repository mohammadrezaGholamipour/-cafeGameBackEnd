from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base


class Buffet(Base):
    __tablename__ = "buffet"  # نام جدول

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="buffet")
    __table_args__ = (
        UniqueConstraint(
            "owner_id",
            "name",
            name="uq_owner_buffet_name"
        ),
    )


from app.models.user import User
