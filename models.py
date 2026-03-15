from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Book(Base):
    __tablename__ = "books"

    id      = Column(Integer, primary_key=True, index=True)
    title   = Column(String(100), nullable=False)
    author  = Column(String(50),  nullable=False)
    rating  = Column(Integer,     nullable=False)
    summary = Column(String(500), nullable=True)


class User(Base):
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True, index=True)
    username        = Column(String(50),  unique=True, nullable=False, index=True)
    email           = Column(String(100), unique=True, nullable=True)
    full_name       = Column(String(100), nullable=True)
    hashed_password = Column(String,      nullable=False)
    disabled        = Column(Boolean,     default=False)