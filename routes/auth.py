from fastapi import APIRouter, HTTPException,Depends
from db import get_connection
from schemas.users import UserCreate, UserResponse,LoginUser
# from routes.auth import router
from utils.security import create_access_token, verify_token

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/add_user/")
async def add_user(data:UserCreate):
    conn = await get_connection()
    try:
        await conn.execute("INSERT INTO users(name, email, phone, password) VALUES ($1, $2, $3, $4)", data.name, data.email, data.phone, data.password)
        return {"message": "User added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()


@router.post("/login_users")
async def login_user(data: LoginUser):
    conn = await get_connection()
    try:
        user = await conn.fetchrow(
            "SELECT * FROM users WHERE email = $1 AND password = $2",
            data.email,
            data.password
        )
        if user:
            token = create_access_token({"sub": str(user["user_id"]), "email": user["email"]})
            return {"message": "Login successful", "access_token": token, "token_type": "bearer"}
        raise HTTPException(status_code=401, detail="Invalid email or password")
    finally:
        await conn.close()


@router.get("/get_users")
async def get_users(user_data: dict = Depends(verify_token)):
    conn = await get_connection()
    try:
        result = await conn.fetch("SELECT * FROM users")
        print("authenticated user :", user_data)
        return [dict(record) for record in result]
    finally:
        await conn.close()


@router.get("/get_user/{user_id}")
async def get_user(user_id: int, user_data: dict = Depends(verify_token)):
    conn = await get_connection()
    try:
        result = await conn.fetchrow("SELECT * FROM users WHERE user_id = $1", user_id)
        if result:
            print("authenticated user :", user_data)
            return dict(result)
        raise HTTPException(status_code=404, detail="User not found")
    finally:
        await conn.close()
