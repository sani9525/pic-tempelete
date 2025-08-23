from pydantic import BaseModel
from typing import Optional

# -------- SELLERS --------
class SellerBase(BaseModel):
    user_id: int
    name: str
    contact_info: str
    location: str
    rating: Optional[float] = None


class SellerCreate(SellerBase):
    pass


class SellerResponse(SellerBase):
    seller_id: int
