# app/crud.py
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from . import models, schemas
from .utils import apply_book_filters


# ---------- Users ----------

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user_in: schemas.UserCreate, hashed_password: str) -> models.User:
    user = models.User(
        email=user_in.email,
        hashed_password=hashed_password,
        is_active=True,
        is_admin=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ---------- Authors ----------

def create_author(db: Session, author_in: schemas.AuthorCreate) -> models.Author:
    author = models.Author(**author_in.model_dump())
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


def list_authors(db: Session) -> List[models.Author]:
    return db.query(models.Author).all()


# ---------- Books ----------

def create_book(db: Session, book_in: schemas.BookCreate) -> models.Book:
    book = models.Book(**book_in.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_book(db: Session, book_id: int) -> Optional[models.Book]:
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def update_book(db: Session, book: models.Book, book_in: schemas.BookUpdate) -> models.Book:
    data = book_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(book, field, value)
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book: models.Book) -> None:
    db.delete(book)
    db.commit()


def list_books(
    db: Session,
    q: Optional[str] = None,
    author_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock_only: bool = False,
) -> List[models.Book]:
    query = db.query(models.Book)
    query = apply_book_filters(
        query=query,
        q=q,
        author_id=author_id,
        min_price=min_price,
        max_price=max_price,
        in_stock_only=in_stock_only,
    )
    return query.all()


# ---------- Cart ----------

def get_cart_items(db: Session, user_id: int) -> List[models.CartItem]:
    return (
        db.query(models.CartItem)
        .filter(models.CartItem.user_id == user_id)
        .all()
    )


def add_to_cart(db: Session, user_id: int, item_in: schemas.CartItemCreate) -> models.CartItem:
    item = (
        db.query(models.CartItem)
        .filter(
            models.CartItem.user_id == user_id,
            models.CartItem.book_id == item_in.book_id,
        )
        .first()
    )

    if item:
        item.quantity += item_in.quantity
    else:
        item = models.CartItem(
            user_id=user_id,
            book_id=item_in.book_id,
            quantity=item_in.quantity,
        )
        db.add(item)

    db.commit()
    db.refresh(item)
    return item


def remove_cart_item(db: Session, user_id: int, item_id: int) -> bool:
    item = (
        db.query(models.CartItem)
        .filter(
            models.CartItem.id == item_id,
            models.CartItem.user_id == user_id,
        )
        .first()
    )
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True


def clear_cart(db: Session, user_id: int) -> List[models.CartItem]:
    items = get_cart_items(db, user_id)
    for item in items:
        db.delete(item)
    db.commit()
    return items


# ---------- Orders ----------

def create_order_from_cart(db: Session, user_id: int) -> Optional[models.Order]:
    cart_items = get_cart_items(db, user_id)
    if not cart_items:
        return None

    order = models.Order(user_id=user_id, status="created")
    db.add(order)
    db.flush()  # get order.id

    total_price = 0.0
    for ci in cart_items:
        unit_price = ci.book.price
        line_total = unit_price * ci.quantity
        total_price += line_total

        order_item = models.OrderItem(
            order_id=order.id,
            book_id=ci.book_id,
            quantity=ci.quantity,
            unit_price=unit_price,
        )
        db.add(order_item)

        # decrease stock (simple)
        if ci.book.in_stock is not None:
            ci.book.in_stock = max(0, ci.book.in_stock - ci.quantity)

    order.total_price = total_price

    # clear cart
    for ci in cart_items:
        db.delete(ci)

    db.commit()
    db.refresh(order)
    return order


def list_orders_for_user(db: Session, user_id: int) -> List[models.Order]:
    return (
        db.query(models.Order)
        .filter(models.Order.user_id == user_id)
        .order_by(models.Order.created_at.desc())
        .all()
    )
