import pytest
from jose import jwt

from app import schemas
from app.config import Settings


def test_signup(client):
    res = client.post("/SignUp", json={"email": "hello@gmail.com", "password": "pass"})

    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == "hello@gmail.com"


def test_signin(client, user):
    res = client.post(
        "/SignIn", data={"username": user["email"], "password": user["password"]}
    )
    new_user = schemas.Token(**res.json())
    assert res.status_code == 200
    payload = jwt.decode(
        new_user.access_token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM]
    )
    id = payload.get("user_id")
    assert id == user["id"]
    assert new_user.token_type == "Bearer"


def test_signout(authorized_client):
    res = authorized_client.post("/SignOut")
    assert res.status_code == 204
    res = authorized_client.get("/GetList")
    assert res.status_code == 401


@pytest.mark.parametrize(
    "email, password, expected_statuscode",
    [
        ("hello@gmail.com", "wrong", 401),
        ("wrong@gmail.com", "pass", 401),
        ("hello@gmail.com", None, 422),
        (None, "pass", 422),
        (None, None, 422),
    ],
)
def test_failed_signin(client, user, email, password, expected_statuscode):
    res = client.post("/SignIn", data={"username": email, "password": password})

    assert res.status_code == expected_statuscode

    if expected_statuscode == 401:
        assert res.json()["detail"] == "Invalid Credentials"
