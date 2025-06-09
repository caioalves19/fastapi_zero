from http import HTTPStatus


def test_root_retornar_ola_mundo(client):
    response = client.get("/")

    assert response.json() == {"message": "Olá, Mundo!"}
    assert response.status_code == HTTPStatus.OK


def test_create_user(client):
    response = client.post(
        "/users",
        json={
            "username": "caioalves",
            "email": "caio@example.com",
            "password": "password",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "username": "caioalves",
        "email": "caio@example.com",
    }


def test_get_users(client):
    response = client.get("/users")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {
                "id": 1,
                "username": "caioalves",
                "email": "caio@example.com",
            }
        ]
    }


def test_get_user_by_id(client):
    response = client.get("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": "caioalves",
        "email": "caio@example.com",
    }


def test_update_user(client):
    response = client.put(
        "/users/1",
        json={
            "username": "cr7",
            "email": "cr7@example.com",
            "password": "password",
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": "cr7",
        "email": "cr7@example.com",
    }


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
    assert response.json() == {"detail": "Não encontrado!"}


def test_delete_user(client):
    response = client.delete("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": "cr7",
        "email": "cr7@example.com",
    }


def test_delete_user_exception(client):
    response = client.delete("/users/2")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Não encontrado!"}
