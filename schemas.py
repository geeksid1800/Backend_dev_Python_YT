from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.types import conint



class UserCreate(BaseModel):
    #Defines what fields are expected from client when creating a new User
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    #Defines what fields are returned to the client when a new User is created/a User is queried for
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
    

class UserLogin(BaseModel):
    email: EmailStr
    password: str



class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True


class PostResponse(BaseModel):
    # Let's say we Don't want to expose ID field to the user
    title: str
    content: str
    published: bool
    created_at: datetime
    user_id: int
    user: UserResponse

    class Config:
        orm_mode = True #Tells the pydantic model to read the data even if it is not a dict and an ORM model instead (as returned by SQLAlchemy)


class Like(BaseModel):
    #Required details  to be passed in when trying to like a post
    post_id: int
    direction: conint(ge=0,le=1) # type: ignore

class LikeResponse(BaseModel):
    Post: PostResponse
    likes: int 

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token : str
    token_type : str


class TokenData(BaseModel):
    id: int
    expiration_time: str
