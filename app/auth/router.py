from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.auth.schemas import UserRegisterSchema, UserWithTokenSchema
from app.auth.db.queries import create_user
from app.auth.security import create_access_token
from app.config import settings
from app.database.dependencies import get_db

TOKEN_TYPE = "bearer"

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register", response_model=UserWithTokenSchema)
async def register_user(
    new_user: UserRegisterSchema,
    db: Session = Depends(get_db),
) -> UserWithTokenSchema:
    try:
        user = create_user(db, user=new_user)
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
