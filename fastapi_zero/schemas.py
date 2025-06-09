from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserPublicSchema(BaseModel):
    username: str
    email: EmailStr
    id: int


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDBSchema(UserSchema):
    id: int


class UserList(BaseModel):
    users: list[UserPublicSchema]
