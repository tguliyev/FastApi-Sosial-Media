from pydantic import BaseModel
from datetime import datetime
from .user import ResponseUser

class RequestPost(BaseModel):
    title: str
    content: str
    published: bool = True

class ResponsePost(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    vote_count: int
    published: bool
    created_at: datetime
    owner: ResponseUser = None