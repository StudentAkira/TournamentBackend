import json

from db.schemas.user.edit_user import EditUserSchema
from .config import *

settings = get_settings()

client = TestClient(app)


def test_get_my_profile():
    token = db.get(User, 1).tokens[0].token
    response = client.get("/api/user/profile", cookies={"token": token})

    client.patch("/api/user/profile", cookies={"token": token},
                 json=json.loads(
                     '{"email":"test@mail.ru",'
                     '"first_name":"Akira",'
                     '"second_name":"Akira",'
                     '"third_name":"Akira",'
                     '"phone":"+375-29-777-77-77",'
                     '"role":"admin",'
                     '"educational_institution":"test"}'
                 ))
    assert response.status_code == 200
    assert response.content == b'{"email":"test@mail.ru",' \
                               b'"first_name":"Akira",' \
                               b'"second_name":"Akira",' \
                               b'"third_name":"Akira",' \
                               b'"phone":"+375-29-777-77-77",' \
                               b'"role":"admin",' \
                               b'"educational_institution":"test"}'


def test_edit_profile():
    token = db.get(User, 1).tokens[0].token
    response = client.patch(
        "/api/user/profile", cookies={"token": token}, json=
        EditUserSchema(
            email="test123@mail.ru",
            password="7689462",
            first_name="test",
            second_name="test",
            third_name="test",
            phone="+375-29-768-94-62",
            educational_institution="test",
        ).model_dump()
    )
    assert response.status_code == 200
    assert response.content == b'{"message":"user data updated"}'
    client.patch("/api/user/profile", cookies={"token": token},
                 json=json.loads(
                     '{"email":"test@mail.ru",'
                     '"first_name":"Akira",'
                     '"second_name":"Akira",'
                     '"third_name":"Akira",'
                     '"phone":"+375-29-777-77-77",'
                     '"role":"admin",'
                     '"educational_institution":"test"}'
                 ))


def test_list_users():
    token = db.get(User, 1).tokens[0].token
    response = client.get("/api/user/users", cookies={"token": token})
    data = response.content.decode('utf-8')
    users = json.loads(data)

    assert response.status_code == 200
    assert len(users) == db.query(User).count()


def test_create_user():
    token = db.get(User, 1).tokens[0].token
    id_ = db.query(User).order_by(User.id.desc()).first().id
    response = client.post("/api/user/create_user", cookies={"token": token},
                           json=json.loads(
                               f'{{"email":"user{int(id_) + 1}@mail.ru",'
                               f'"password": "user{int(id_) + 1}@mail.ru",'
                               f'"first_name":"user{int(id_) + 1}",'
                               f'"second_name":"user{int(id_) + 1}",'
                               f'"third_name":"user{int(id_) + 1}",'
                               '"phone":"+375-29-777-77-77",'
                               '"role":"specialist",'
                               '"educational_institution":"test"}'
                           ))
    assert response.status_code == 200
    test_list_users()


def create_specialist():
    token = db.get(User, 1).tokens[0].token
    id_ = db.query(User).order_by(User.id.desc()).first().id
    response = client.post("/api/user/create_user", cookies={"token": token},
                           json=json.loads(
                               f'{{"email":"user{int(id_) + 1}@mail.ru",'
                               f'"password": "user{int(id_) + 1}@mail.ru",'
                               f'"first_name":"user{int(id_) + 1}",'
                               f'"second_name":"user{int(id_) + 1}",'
                               f'"third_name":"user{int(id_) + 1}",'
                               '"phone":"+375-29-777-77-77",'
                               '"role":"specialist",'
                               '"educational_institution":"test"}'
                           ))
    assert response.status_code == 200
    test_list_users()


# def test_not_admin_create_user():
#     create_specialist()
#
#     user_db = db.query(User).filter(User.role != "admin").first()
#     response = client.post("/api/auth/login", json={"email": user_db.email, "password": f"user{user_db.id + 1}@mail.ru"})
#
#     assert response.status_code == 200
#     assert "set-cookie" in response.headers
#
#     token = user_db.tokens[0].token
#     id_ = db.query(User).order_by(User.id.desc()).first().id
#     response = client.post("/api/user/create_user", cookies={"token": token},
#                            json=json.loads(
#                                f'{{"email":"user{int(id_) + 1}@mail.ru",'
#                                f'"password": "user{int(id_) + 1}@mail.ru",'
#                                f'"first_name":"user{int(id_) + 1}",'
#                                f'"second_name":"user{int(id_) + 1}",'
#                                f'"third_name":"user{int(id_) + 1}",'
#                                '"phone":"+375-29-777-77-77",'
#                                '"role":"admin",'
#                                '"educational_institution":"test"}'
#                            ))
#     assert response.status_code == 200
#     test_list_users()
#
#     response = client.post("/api/auth/logout", cookies={"token": token})
#     assert response.status_code == 200
#     assert token not in set(token_db.token for token_db in db.get(User, 1).tokens)

