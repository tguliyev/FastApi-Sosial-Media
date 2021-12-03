from pydantic import EmailStr, BaseModel


class RequestLogin(BaseModel):
    email: EmailStr
    password: str