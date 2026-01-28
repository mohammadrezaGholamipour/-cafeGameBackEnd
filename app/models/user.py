from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    userName = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    mobile = Column(String, nullable=False)
    consoles = relationship("Console", back_populates="owner")
    buffet = relationship("Buffet", back_populates="owner")

from app.models.console import Console
from app.models.buffet import Buffet