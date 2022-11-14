from sqlalchemy.orm import Session
from ..models.user_model import UserModel
from ..schemas.user_schema import UserCreate
from ..utils.crypto import get_hashed_password


def get_user(db: Session, email: str) -> UserModel:
    return db.query(UserModel).filter(UserModel.email == email).first()


def create(db: Session, user: UserCreate):
    hashed = get_hashed_password(user.password)
    db_user = UserModel(email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
