from pydantic import BaseModel, EmailStr, Field
from fastapi import HTTPException

class UserBase(BaseModel):
    email: EmailStr
    name= str =Field(..., description= "Username",min_length=4, max_length=50)
    password= str =Field(..., description= "Password",min_length=4, max_length=50)
    

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int
    class Config:
        orm_model = True

class UserUpdate(UserBase):
    pass
