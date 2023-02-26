from datetime import datetime

from pydantic import BaseModel, EmailStr


class BaseResource(BaseModel):
    title: str
    content: str


class ResourceCreate(BaseResource):
    pass


class ResourceUpdate(BaseResource):
    pass


class Resource(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserSignIn(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int = None
