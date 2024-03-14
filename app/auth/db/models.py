from sqlalchemy import Boolean, Column, DateTime, func, Integer, String

from app.database.config import ModelBase


class UserModel(ModelBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_admin = Column(Boolean, default=False)
