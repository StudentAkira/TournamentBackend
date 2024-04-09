from .config import *

settings = get_settings()

client = TestClient(app)


def test_logout():
    token_to_logout = db.get(User, 1).tokens[0].token
    response = client.post("/api/auth/logout", cookies={"token": token_to_logout})
    assert response.status_code == 200
    assert token_to_logout not in set(token_db.token for token_db in db.get(User, 1).tokens)


def test_wrong_token_logout():
    token_to_logout = "123"
    response = client.post("/api/auth/logout", cookies={"token": token_to_logout})
    assert response.status_code == 500
    assert response.content == b'{"detail":{"error":"Token is invalid"}}'
