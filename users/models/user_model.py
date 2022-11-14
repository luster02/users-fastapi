from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from ..database.connection import Base


class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime,  server_default=func.now())
