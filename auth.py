from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()

# Hashed dummy password — used to prevent timing attacks
DUMMY_HASH = password_hash.hash("Qwerty123!")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# --- Password utils ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)


# --- User lookup ---
def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


# --- Authenticate: verify username + password ---
def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        verify_password(password, DUMMY_HASH)  
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# --- JWT utils ---
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# --- Dependencies ---
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db:    Annotated[Session, Depends(get_db)]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[models.User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


CurrentUser = Annotated[models.User, Depends(get_current_active_user)]