# app/utils.py
from typing import Optional

from fastapi import BackgroundTasks
from sqlalchemy.orm import Query


def apply_book_filters(
    query: Query,
    q: Optional[str] = None,
    author_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock_only: bool = False,
) -> Query:
    from .models import Book  # local import to avoid circulars

    if q:
        pattern = f"%{q.lower()}%"
        query = query.filter(Book.title.ilike(pattern))
    if author_id is not None:
        query = query.filter(Book.author_id == author_id)
    if min_price is not None:
        query = query.filter(Book.price >= min_price)
    if max_price is not None:
        query = query.filter(Book.price <= max_price)
    if in_stock_only:
        query = query.filter(Book.in_stock > 0)
    return query


# Very simple "email" sender (just logs)
def send_order_email(email: str, order_id: int) -> None:
    # Here you would integrate actual email provider.
    print(f"[EMAIL] Sent order confirmation to {email} for order #{order_id}")


def schedule_order_email(background_tasks: BackgroundTasks, email: str, order_id: int) -> None:
    background_tasks.add_task(send_order_email, email, order_id)
