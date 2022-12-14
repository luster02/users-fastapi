from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserSchema(UserBase):
    user_id: int

    class Config:
        orm_mode = True
