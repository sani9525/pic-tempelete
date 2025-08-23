from pydantic import BaseModel, EmailStr
from typing import Optional


# -------- USERS --------

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[int] = 0
    password: str




class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    user_id: int