from .config import *

client = TestClient(app)


def test_login():
    response = client.post("/api/auth/login", json={"email": "test@mail.ru", "password": "7689462"})
    assert response.status_code == 200
    assert "set-cookie" in response.headers


def test_wrong_email_login():
    response = client.post("/api/auth/login", json={"email": "testxeqwcrvwtrebyber@mail.ru", "password": "7689462"})
    assert response.status_code == 404
    assert response.content == b'{"detail":{"error":"user not found"}}'


def test_wrong_password_login():
    response = client.post("/api/auth/login", json={"email": "test@mail.ru", "password": "76894621"})
    assert response.status_code == 401
    assert response.content == b'{"detail":{"error":"invalid password"}}'
