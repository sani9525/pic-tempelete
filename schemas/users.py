from pydantic import BaseModel, EmailStr


# -------- USERS --------

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: int
    password: str




class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    user_id: int