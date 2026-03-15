from datetime import timedelta
from typing import Annotated, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

import models
import schemas
import auth
from database import engine, DbDep

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# ========== AUTH ROUTES ==========

@app.post("/register", response_model=schemas.UserResponse, status_code=201)
async def register(user: schemas.UserCreate, db: DbDep):
    existing = auth.get_user(db, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=auth.get_password_hash(user.password),
        disabled=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DbDep
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@app.get("/users/me", response_model=schemas.UserResponse)
async def read_users_me(current_user: auth.CurrentUser):
    return current_user


# ========== BOOK ROUTES ==========

@app.get("/books", response_model=list[schemas.BookResponse])
async def get_books(db: DbDep):
    return db.query(models.Book).all()


@app.get("/books/search/", response_model=list[schemas.BookResponse])
async def search_books(
    db:     DbDep,
    rating: Optional[int] = None,
    author: Optional[str] = None,
    limit:  int = 10,
):
    query = db.query(models.Book)
    if rating is not None:
        query = query.filter(models.Book.rating == rating)
    if author is not None:
        query = query.filter(models.Book.author.ilike(f"%{author}%"))
    return query.limit(limit).all()


@app.get("/books/{book_id}", response_model=schemas.BookResponse)
async def get_book(book_id: int, db: DbDep):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books", response_model=schemas.BookResponse, status_code=201)
async def create_book(
    book:         schemas.BookCreate,
    db:           DbDep,
    current_user: auth.CurrentUser        # 🔒 protected
):
    new_book = models.Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@app.put("/books/{book_id}", response_model=schemas.BookResponse)
async def update_book(
    book_id:      int,
    updated:      schemas.BookCreate,
    db:           DbDep,
    current_user: auth.CurrentUser        # 🔒 protected
):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in updated.model_dump().items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book


@app.delete("/books/{book_id}", response_model=schemas.Message)
async def delete_book(
    book_id:      int,
    db:           DbDep,
    current_user: auth.CurrentUser        
):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"detail": f"Book {book_id} deleted successfully"}