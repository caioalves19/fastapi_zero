from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fastapi_zero.schemas import (
    Message,
    UserDBSchema,
    UserList,
    UserPublicSchema,
    UserSchema,
)

app = FastAPI()
database = []


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Olá, Mundo!"}


@app.get("/users", status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {"users": database}


@app.post(
    "/users", status_code=HTTPStatus.CREATED, response_model=UserPublicSchema
)
def create_user(user: UserSchema):
    user_with_id = UserDBSchema(
        username=user.username,
        email=user.email,
        password=user.password,
        id=len(database) + 1,
    )
    database.append(user_with_id)
    return user_with_id


@app.put(
    "/users/{user_id}",
    status_code=HTTPStatus.OK,
    response_model=UserPublicSchema,
)
def update_user(user_id: int, user: UserSchema):
    user_with_id = UserDBSchema(**user.model_dump(), id=user_id)

    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Não encontrado!"
        )

    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete(
    "/users/{user_id}",
    status_code=HTTPStatus.OK,
    response_model=UserPublicSchema,
)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Não encontrado!"
        )
    user_deleted = database[user_id - 1]
    del database[user_id - 1]
    return user_deleted


@app.get(
    "/users/{user_id}",
    status_code=HTTPStatus.OK,
    response_model=UserPublicSchema,
)
def get_user_by_id(user_id: int):
    return database[user_id - 1]
