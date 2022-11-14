import os
from dotenv import load_dotenv
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..database.connection import Base
from ..main import app, get_db

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.environ["SQLALCHEMY_DATABASE_URL"]

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True, scope="function")
def drop_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


def test_signin(drop_db):
    client.post(
        "/signup", json={"email": "test@test.com", "password": "test"})
    response = client.post(
        "/signin", json={"email": "test@test.com", "password": "test"})
    assert response.status_code == 200


def test_singup(drop_db):
    response = client.post(
        "/signup", json={"email": "test@test.com", "password": "test"})
    assert response.status_code == 201
