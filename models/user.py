from typing import Any
from pydantic import BaseModel, EmailStr
from datetime import datetime

class RequestUser(BaseModel):
    email: EmailStr
    password: str
    

class ResponseUser(BaseModel):
    id: int
    email: str
    created_at: datetime

class UserModel(BaseModel):
    id: int
    email: str
    password: str
    created_at: datetime
