from http import HTTPStatus

from fastapi.testclient import TestClient
from jwt import decode

from app.security import SECRET_KEY, create_access_token


def test_jwt():
    data = {"test": "test"}
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=["HS256"])

    assert decoded["test"] == data["test"]
    assert "exp" in decoded


def test_jwt_invalid_token(client: TestClient):
    response = client.delete(
        "/users/1",
        headers={"Authorization": "Bearer token-invalido"},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}
