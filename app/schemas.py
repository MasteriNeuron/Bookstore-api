# app/schemas.py
from datetime import datetime, timedelta
from typing import List, Optional

from pydantic import BaseModel, EmailStr, ConfigDict


# ---------- User ----------

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ---------- Author ----------

class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ---------- Book ----------

class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    in_stock: int = 0
    author_id: Optional[int] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    in_stock: Optional[int] = None
    author_id: Optional[int] = None


class BookRead(BookBase):
    id: int
    author: Optional[AuthorRead] = None

    model_config = ConfigDict(from_attributes=True)


# ---------- Cart ----------

class CartItemBase(BaseModel):
    book_id: int
    quantity: int = 1


class CartItemCreate(CartItemBase):
    pass


class CartItemRead(CartItemBase):
    id: int
    book: BookRead

    model_config = ConfigDict(from_attributes=True)


# ---------- Orders ----------

class OrderItemRead(BaseModel):
    id: int
    book: BookRead
    quantity: int
    unit_price: float

    model_config = ConfigDict(from_attributes=True)


class OrderRead(BaseModel):
    id: int
    created_at: datetime
    status: str
    total_price: float
    items: List[OrderItemRead]

    model_config = ConfigDict(from_attributes=True)


# ---------- Auth / Token ----------

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sub: Optional[str] = None
    exp: Optional[datetime] = None
