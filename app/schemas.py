from datetime import datetime
from re import S
from typing import Optional
from annotated_types import BaseMetadata
from pydantic import BaseModel, EmailStr, conint, Field


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True 

class PostCreate(PostBase):
    pass


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr

class PostResponse(PostBase):
    created_at: datetime
    user_id: int
    owner: UserResponse


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: int = Field(..., ge=0, le=1)

class VoteResponse(BaseModel):
    Post: PostResponse
    votes: int
