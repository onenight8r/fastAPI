
from pydantic import BaseModel,EmailStr
from typing import Optional

class Post(BaseModel):
    title:str
    content:str
    published:bool = True

class Users(BaseModel):
    email:str
    password:str

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id: int
    email:EmailStr

    class Config: 
        orm_mode=True

class UserLogin(BaseModel):
    email: EmailStr
    password:str

class Token(BaseModel):
    access_token: str
    token_type : str

class ToeknData(BaseModel):
    id: Optional[str]=None