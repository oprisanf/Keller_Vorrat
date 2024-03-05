from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric, Date
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    quantity = Column(Integer)
    item_name =Column(String, index=True)
    description = Column(String)
    price = Column(Numeric, index=True)
    expiry_date = Column(Date, index=True)
    tag = Column(String, index = True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    deleted = Column(Boolean, default= False)
    owner = relationship("User", back_populates="items", foreign_keys=[owner_id])