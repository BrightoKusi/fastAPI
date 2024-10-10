from datetime import datetime
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True 

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    created_at: datetime

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    user_name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    first_name: str
    last_name: str
    user_name: str
    email: EmailStr
