from pydantic import BaseModel

class RequestVote(BaseModel):
    post_id: int
    direction: bool = True