from fastapi import FastAPI
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .schemas import user_schema

from .models import user_model
from .database import user_repository, connection
from .schemas import jwt_schema, user_schema
from .utils import crypto

user_model.Base.metadata.create_all(bind=connection.engine)

app = FastAPI()


def get_db():
    db = connection.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/signin", response_model=jwt_schema.JwtModel)
def signin(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_repository.get_user(db=db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=403, detail="Email or password wrong")
    if not crypto.verify_hashed(password=user.password, hashed_password=db_user.hashed_password):
        raise HTTPException(status_code=403, detail="Email or password wrong")
    token = jwt_schema.JwtModel.custom_encode(user=db_user)
    print("token", token)
    return jwt_schema.JwtModel(token=token)


@app.post("/signup", response_model=jwt_schema.JwtModel, status_code=201)
def signup(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_repository.get_user(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="Email alreay exists")
    user_created = user_repository.create(db=db, user=user)
    token = jwt_schema.JwtModel.custom_encode(user=user_created)
    return jwt_schema.JwtModel(token=token)
