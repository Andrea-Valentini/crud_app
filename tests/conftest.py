from fastapi.testclient import TestClient
from pytest import fixture

from app import models
from app.database import Base, get_db
from app.main import app
from app.oauth2 import create_access_token

from .database import TestingSessionLocal, engine


@fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@fixture
def user(client):
    user_data = {"email": "hello@gmail.com", "password": "pass"}

    res = client.post("/SignUp", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@fixture
def token(user):
    return create_access_token({"user_id": user["id"]})


@fixture
def authorized_user(user, token, session):
    user = session.query(models.User).filter(models.User.email == user["email"]).first()
    user.access_token = token
    session.commit()


@fixture
def authorized_client(client, token, authorized_user):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@fixture
def resources(session):
    resources = [
        {
            "title": "sample title 1",
            "content": "sample content 1",
            "created_at": "2023-01-01T12:00:00.000",
        },
        {
            "title": "sample title 2",
            "content": "sample content 2",
            "created_at": "2023-01-02T12:00:00.000",
        },
        {
            "title": "sample title 3",
            "content": "sample content 3",
            "created_at": "2023-01-03T12:00:00.000",
        },
        {
            "title": "sample title 3",
            "content": "sample content 4",
            "created_at": "2023-01-04T12:00:00.000",
        },
    ]

    def create_model(res):
        return models.Resource(**res)

    session.add_all(list(map(create_model, resources)))

    session.commit()
    return resources
