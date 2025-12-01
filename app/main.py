# app/main.py
from typing import List, Optional

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import auth, crud, models, schemas
from .auth import get_current_active_user, get_current_admin
from .database import Base, engine, get_db
from .utils import schedule_order_email
# Auto create admin user (only if none exists)
from .database import SessionLocal
from .auth import get_password_hash
from .crud import get_user_by_email, create_user
from .schemas import UserCreate

# Create tables on startup (simple dev-style)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Online Bookstore API",
    version="0.1.0",
    description="A simple FastAPI-based bookstore example.",
)


# ---------- Health ----------

@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok", "message": "Online Bookstore API"}


# ---------- Auth & Users ----------

@app.post("/auth/register", response_model=schemas.UserRead, tags=["auth"])
def register_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    existing = crud.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    hashed_pw = auth.get_password_hash(user_in.password)
    user = crud.create_user(db, user_in, hashed_pw)
    return user


def create_default_admin():
    db = SessionLocal()
    admin_email = "admin@bookstore.com"
    admin_password = "admin123"

    if not get_user_by_email(db, admin_email):
        print("[INIT] Creating default admin:", admin_email)
        hashed = get_password_hash(admin_password)
        user = create_user(db, UserCreate(email=admin_email, password=admin_password), hashed)
        user.is_admin = True
        db.commit()
    db.close()

create_default_admin()

@app.post("/auth/token", response_model=schemas.Token, tags=["auth"])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # We treat username as email for simplicity
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = auth.create_access_token(subject=user.email)
    return schemas.Token(access_token=token, token_type="bearer")


@app.get("/users/me", response_model=schemas.UserRead, tags=["users"])
async def read_me(
    current_user: models.User = Depends(get_current_active_user),
):
    return current_user


# ---------- Authors ----------

@app.post("/authors", response_model=schemas.AuthorRead, tags=["authors"])
def create_author(
    author_in: schemas.AuthorCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_admin),
):
    return crud.create_author(db, author_in)


@app.get("/authors", response_model=List[schemas.AuthorRead], tags=["authors"])
def list_authors(
    db: Session = Depends(get_db),
):
    return crud.list_authors(db)


# ---------- Books ----------

@app.post("/books", response_model=schemas.BookRead, tags=["books"])
def create_book(
    book_in: schemas.BookCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_admin),
):
    return crud.create_book(db, book_in)


@app.get("/books", response_model=List[schemas.BookRead], tags=["books"])
def list_books(
    q: Optional[str] = None,
    author_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock_only: bool = False,
    db: Session = Depends(get_db),
):
    return crud.list_books(
        db=db,
        q=q,
        author_id=author_id,
        min_price=min_price,
        max_price=max_price,
        in_stock_only=in_stock_only,
    )


@app.get("/books/{book_id}", response_model=schemas.BookRead, tags=["books"])
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.put("/books/{book_id}", response_model=schemas.BookRead, tags=["books"])
def update_book(
    book_id: int,
    book_in: schemas.BookUpdate,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_admin),
):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.update_book(db, book, book_in)


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["books"])
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_admin),
):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    crud.delete_book(db, book)
    return None


# ---------- Cart ----------

@app.get("/cart", response_model=List[schemas.CartItemRead], tags=["cart"])
def get_cart(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    return crud.get_cart_items(db, current_user.id)


@app.post("/cart", response_model=schemas.CartItemRead, tags=["cart"])
def add_cart_item(
    item_in: schemas.CartItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    # basic stock check
    book = crud.get_book(db, item_in.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.in_stock is not None and book.in_stock < item_in.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")
    return crud.add_to_cart(db, current_user.id, item_in)


@app.delete("/cart/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["cart"])
def remove_cart_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    ok = crud.remove_cart_item(db, current_user.id, item_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return None


# ---------- Orders ----------

@app.post("/orders", response_model=schemas.OrderRead, tags=["orders"])
def create_order(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    order = crud.create_order_from_cart(db, current_user.id)
    if not order:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Email notification in background
    schedule_order_email(background_tasks, current_user.email, order.id)
    return order


@app.get("/orders/my", response_model=List[schemas.OrderRead], tags=["orders"])
def list_my_orders(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user),
):
    return crud.list_orders_for_user(db, current_user.id)
