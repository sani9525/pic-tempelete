from fastapi import APIRouter, HTTPException,Depends
from db import get_connection
from schemas.sellers import SellerCreate, SellerResponse
# from routes.auth import router
from utils.security import create_access_token, verify_token

router = APIRouter(prefix="/sellers", tags=["Sellers"])


@router.post("/create_seller")
async def create_seller(seller: SellerCreate,user_data: dict = Depends(verify_token)):
    conn = await get_connection()
    print("authenticated user :", user_data)
    try:
        result = await conn.execute(
            "INSERT INTO sellers (user_id, name, contact_info, location, rating) VALUES ($1, $2, $3, $4, $5)",
            seller.user_id,
            seller.name,
            seller.contact_info,
            seller.location,
            seller.rating
        )

        return {"message": "Seller created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()



@router.get("/get_sellers")
async def get_sellers(user_data: dict = Depends(verify_token)):
    conn = await get_connection()
    print("authenticated user :", user_data)
    try:
        result = await conn.fetch("SELECT * FROM sellers")
        sellers = [dict(row) for row in result]
        return sellers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await conn.close()