from pydantic import BaseModel
from datetime import date,timedelta
from typing import List, Optional


class ItemBase(BaseModel):
    id:int = None
    quantity:int
    item_name: str
    description: Optional[str] = "Essbar"
    price: float = None
    expiry_date: date = date.today() + timedelta(days=365*2)
    tag: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    # item_id:Optional[int]
    # owner_id: int
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True