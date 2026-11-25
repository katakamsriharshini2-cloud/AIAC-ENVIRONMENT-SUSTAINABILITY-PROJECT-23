import pytest
from app.api.auth_routes import register, login
from app.schemas import UserRegister, UserLogin
from app.auth import verify_password, get_password_hash, create_access_token
from fastapi import HTTPException

def test_password_hashing():
    pwd = "Admin@123456"
    h = get_password_hash(pwd)
    assert verify_password(pwd, h) is True
    assert verify_password("WrongPassword", h) is False

def test_create_access_token():
    token = create_access_token({"sub": "admin@ecosphere.org", "role": "admin"})
    assert isinstance(token, str)
    assert len(token) > 20

def test_login_admin(db_session):
    login_in = UserLogin(email="admin@ecosphere.org", password="Admin@123456")
    res = login(login_in, db=db_session)
    assert res["token_type"] == "bearer"
    assert res["user"].email == "admin@ecosphere.org"
    assert res["user"].role == "admin"

def test_login_officer(db_session):
    login_in = UserLogin(email="officer@ecosphere.org", password="Officer@123456")
    res = login(login_in, db=db_session)
    assert res["user"].role == "environmental_officer"

def test_login_invalid_password(db_session):
    login_in = UserLogin(email="admin@ecosphere.org", password="InvalidPassword!")
    with pytest.raises(HTTPException) as exc:
        login(login_in, db=db_session)
    assert exc.value.status_code == 401

def test_register_duplicate_user(db_session):
    reg_in = UserRegister(
        email="admin@ecosphere.org",
        password="SomePassword123",
        full_name="Duplicate Admin",
        role="admin"
    )
    with pytest.raises(HTTPException) as exc:
        register(reg_in, db=db_session)
    assert exc.value.status_code == 400
