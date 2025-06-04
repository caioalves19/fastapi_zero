from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserPublicSchema(BaseModel):
    user: str
    email: EmailStr
    id: int


class UserSchema(BaseModel):
    user: str
    email: EmailStr
    password: str


class UserDBSchema(UserSchema):
    id: int


class UserList(BaseModel):
    users: list[UserPublicSchema]
