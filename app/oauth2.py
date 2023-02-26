from collections import deque
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import models, schemas
from .config import Settings
from .database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/SignIn")

token_blacklist = deque()


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM
    )

    return encoded_jwt


def verify_access_token(token: str, credentials_exception, db):
    try:
        payload = jwt.decode(
            token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM]
        )
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == id).first()
    if user.access_token is None:
        raise credentials_exception

    return token_data


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_access_token(token, credentials_exception, db)
