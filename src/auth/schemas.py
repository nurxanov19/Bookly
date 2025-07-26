from pydantic import BaseModel, Field, field_validator
import uuid
from datetime import date, datetime


class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=15)
    email: str = Field(max_length=50)
    password: str = Field(max_length=254, min_length=6)

    
class UserModel(BaseModel):
    uid: uuid.UUID 

    username: str
    email: str
    first_name: str
    last_name: str
    password_hash: str = Field(exclude=True)
    is_verified: bool 
    created_at: datetime 
    updated_at: datetime 


class UserLoginModel(BaseModel):
    email: str = Field(max_length=20)
    password: str = Field(max_length=254, min_length=6)