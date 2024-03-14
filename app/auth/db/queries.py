from sqlalchemy.orm import Session

from app.auth.db.models import UserModel
from app.auth.schemas import UserSchema, UserRegisterSchema
from app.auth.security import hash_password


def create_user(db: Session, user: UserRegisterSchema) -> UserSchema:
    user = UserModel(
        username=user.username,
        name=user.name,
        hashed_password=hash_password(user.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
