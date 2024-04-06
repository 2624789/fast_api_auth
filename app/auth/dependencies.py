from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.auth.db import UserModel
from app.auth.schemas import UserSchema
from app.database.dependencies import get_db
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

TokenDep = Annotated[str, Depends(oauth2_scheme)]


async def get_current_user(
    token: TokenDep, db: Session = Depends(get_db)
) -> UserSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=[{"msg":"Could not validate credentials."}],
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.hash_algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = UserModel.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user


CurrentUserDep = Annotated[UserSchema, Depends(get_current_user)]
