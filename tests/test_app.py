from http import HTTPStatus

from fastapi_zero.schemas import UserPublicSchema


def test_root_retornar_ola_mundo(client):
    response = client.get("/")

    assert response.json() == {"message": "Olá, Mundo!"}
    assert response.status_code == HTTPStatus.OK


def test_create_user(client):
    response = client.post(
        "/users",
        json={
            "username": "caioalves123",
            "email": "caioalves123@example.com",
            "password": "password",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "username": "caioalves123",
        "email": "caioalves123@example.com",
    }


def test_create_user_exception(client, user):
    response = client.post(
        "/users",
        json={
            "username": "cr7",
            "email": "caioalves123@example.com",
            "password": "password",
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Username or e-mail already exists"}


def test_get_users(client):
    response = client.get("/users")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_get_users_with_users(client, user):
    user_schema = UserPublicSchema.model_validate(user).model_dump()
    response = client.get("/users")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_get_user_by_id(client, user):
    user_schema = UserPublicSchema.model_validate(user).model_dump()
    response = client.get("/users/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_get_user_by_id_exception(client):
    response = client.get("/users/1")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_update_user(client, user):
    user_schema = UserPublicSchema.model_validate(user).model_dump()
    response = client.put(
        "/users/1",
        json={
            "username": "cr7",
            "email": "cr7@example.com",
            "password": "password",
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_update_user_exception(client):
    response = client.put(
        "/users/2",
        json={
            "username": "cr7",
            "email": "cr7@example.com",
            "password": "password",
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_delete_user(client, user):
    user_schema = UserPublicSchema.model_validate(user).model_dump()
    response = client.delete("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_delete_user_exception(client):
    response = client.delete("/users/2")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_update_integrity_exception(client, user):
    client.post(
        "/users",
        json={
            "username": "caioalves123",
            "email": "caioalves123@example.com",
            "password": "password",
        },
    )

    response = client.put(
        f"/users/{user.id}",
        json={
            "username": "caioalves123",
            "email": "cr7@example.com",
            "password": "password",
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Username or e-mail already exists"}
