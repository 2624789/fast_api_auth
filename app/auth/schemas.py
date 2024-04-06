from pydantic import BaseModel, EmailStr


class UserBaseSchema(BaseModel):
    username: EmailStr
    name: str


class UserSchema(UserBaseSchema):
    is_admin: bool

    class Config:
        from_attributes = True


class UserWithTokenSchema(UserSchema):
    access_token: str
    token_type: str


class UserRegisterSchema(UserBaseSchema):
    password: str
