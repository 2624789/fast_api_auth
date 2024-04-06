from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.auth.db import UserModel
from app.auth.dependencies import CurrentUserDep
from app.auth.schemas import UserRegisterSchema, UserSchema, UserWithTokenSchema
from app.auth.security import create_access_token
from app.config import settings
from app.database.dependencies import get_db

TOKEN_TYPE = "bearer"

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.get("/current-user", response_model=UserSchema)
async def get_current_user(current_user: CurrentUserDep) -> UserSchema:
    return current_user


@router.post("/login", response_model=UserWithTokenSchema)
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> UserWithTokenSchema:
    user = UserModel.authenticate_user(
        db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[{"msg":"Incorrect email or password"}],
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes
    )
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {
        **user.__dict__,
        "access_token": access_token,
        "token_type": TOKEN_TYPE
    }


@router.post("/register", response_model=UserWithTokenSchema)
async def register_user(
    new_user: UserRegisterSchema,
    db: Session = Depends(get_db),
) -> UserWithTokenSchema:
    try:
        user = UserModel.create_user(db, user=new_user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[{"msg": "User already exists"}],
        )
    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes
    )
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        **user.__dict__,
        "access_token": access_token,
        "token_type": TOKEN_TYPE
    }
