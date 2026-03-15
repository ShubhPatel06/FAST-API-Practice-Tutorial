from pydantic import BaseModel, Field
from typing import Annotated, Optional


# --- Token schemas ---
class Token(BaseModel):
    access_token: str
    token_type:   str


class TokenData(BaseModel):
    username: str | None = None


# --- User schemas ---
class UserCreate(BaseModel):
    username:  str = Field(min_length=3, max_length=50)
    password:  str = Field(min_length=6)
    email:     Optional[str] = None
    full_name: Optional[str] = None


class UserResponse(BaseModel):
    id:        int
    username:  str
    email:     Optional[str] = None
    full_name: Optional[str] = None
    disabled:  bool | None = None

    class Config:
        from_attributes = True


# --- Book schemas ---
class BookCreate(BaseModel):
    title:   str = Field(min_length=1, max_length=100)
    author:  str = Field(min_length=1, max_length=50)
    rating:  int = Field(ge=1, le=5)
    summary: Optional[str] = Field(default=None, max_length=500)


class BookResponse(BaseModel):
    id:      int
    title:   str
    author:  str
    rating:  int
    summary: Optional[str] = None

    class Config:
        from_attributes = True


class Message(BaseModel):
    detail: str