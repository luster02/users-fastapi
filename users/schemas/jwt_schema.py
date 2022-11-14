import os
from dotenv import load_dotenv
from pydantic import BaseModel
from jwt import encode

load_dotenv()

JWT_KEY = os.environ["JWT_KEY"]


class JwtModel(BaseModel):
    def custom_encode(user):
        return encode({"id": user.user_id, "email": user.email},
                      JWT_KEY, algorithm="HS256")

    token: str
