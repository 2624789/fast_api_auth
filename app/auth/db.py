from typing import Union

from sqlalchemy import Boolean, Column, DateTime, func, Integer, String
from sqlalchemy.orm import Session

from app.auth.schemas import UserSchema, UserRegisterSchema
from app.auth.security import hash_password, verify_password
from app.database.config import ModelBase


class UserModel(ModelBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_admin = Column(Boolean, default=False)

    @classmethod
    def authenticate_user(
        cls, db, username: str, password: str
    ) -> Union[UserSchema, bool]:
        user = cls.get_user_by_username(db, username=username)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user
    
    @classmethod
    def create_user(cls, db: Session, user: UserRegisterSchema) -> UserSchema:
        user = cls(
            username=user.username,
            name=user.name,
            hashed_password=hash_password(user.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @classmethod
    def get_user_by_username(cls, db: Session, username: str) -> UserSchema:
        return db.query(cls).filter(cls.username == username).first()
