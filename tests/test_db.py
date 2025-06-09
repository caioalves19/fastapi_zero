from dataclasses import asdict

from sqlalchemy import select

from fastapi_zero.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username="Caio Alves",
            email="teste@gmail.com",
            password="teste",
        )

        session.add(new_user)
        session.commit()

        user = session.scalar(
            select(User).where(User.username == "Caio Alves")
        )

        assert asdict(user) == {
            "id": 1,
            "username": "Caio Alves",
            "email": "teste@gmail.com",
            "password": "teste",
            "created_at": time,
            "updated_at": time,
        }
