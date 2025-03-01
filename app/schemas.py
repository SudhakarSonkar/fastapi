from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
    
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
    
class PostCreate(PostBase):
    owner_id: int


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    
    
    class Config:
        orm_mode = True
        from_attributes = True 
        
        
class PostOut(BaseModel):
    post: Post
    votes: int
    
    class Config:
        orm_mode = True
        
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
        
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    
class Token(BaseModel):
    access_token: str
    token_type: str
    

class TokenData(BaseModel):
    id: int
    
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # type: ignore