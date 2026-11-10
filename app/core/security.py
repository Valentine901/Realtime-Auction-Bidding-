from fastapi.security import APIKeyCookie
from fastapi import Depends, HTTPException, status, Response 
from sqlalchemy.ext.asyncio import AsyncSession 
from app.models import User 
from app.db.session import get_session
from app.repositories.user import UserRepository
from datetime import timezone, timedelta, datetime 
from pwdlib import PasswordHash
from app.core.exceptions import InvalidToken
from app.core.config import setting 
import jwt
from app.db.session import get_session

cookie_scheme = APIKeyCookie(name="access_token", auto_error=True, scheme_name=None, description="For authorization and authentication")

pwd_scheme = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return pwd_scheme.hash(password)

def verify_password(plain_pass: str, hashed_pass: str) -> bool:
    return pwd_scheme.verify(plain_pass, hashed_pass)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=1440)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    try:
        payload: dict = jwt.decode(token, key=setting.SECRET_KEY, algorithms=[setting.ALGORITHM])
        return payload 
    except jwt.InvalidTokenError:
        raise InvalidToken

    
