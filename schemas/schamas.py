from pydantic import BaseModel, EmailStr, Field, HttpUrl
from typing import Optional
from enum import Enum
from datetime import datetime


# -------- ENUMS --------
class TemplateType(str, Enum):
    frame = "frame"
    poster = "poster"
    collage = "collage"
    gift = "gift"

class OrderStatus(str, Enum):
    pending = "Pending"
    processing = "Processing"
    shipped = "Shipped"
    delivered = "Delivered"
    cancelled = "Cancelled"


class PaymentStatus(str, Enum):
    pending = "Pending"
    paid = "Paid"
    refunded = "Refunded"


class DeliveryStatus(str, Enum):
    shipped = "Shipped"
    in_transit = "In Transit"
    delivered = "Delivered"

# -------- SELLERS --------
class SellerBase(BaseModel):
    name: str
    contact_info: str
    location: str
    rating: Optional[float] = None


class SellerCreate(SellerBase):
    pass


class SellerResponse(SellerBase):
    seller_id: int


# -------- TEMPLATES --------
class TemplateBase(BaseModel):
    name: str
    type: TemplateType
    price: float
    preview_image: Optional[HttpUrl] = None
    design_file: Optional[HttpUrl] = None
    seller_id: int


class TemplateCreate(TemplateBase):
    pass


class TemplateResponse(TemplateBase):
    template_id: int


# -------- ORDERS --------
class OrderBase(BaseModel):
    user_id: int
    template_id: int
    uploaded_photo_url: Optional[HttpUrl] = None
    order_status: OrderStatus = OrderStatus.pending
    payment_status: PaymentStatus = PaymentStatus.pending
    total_price: float
    shipping_partner: Optional[str] = None
    tracking_id: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderResponse(OrderBase):
    order_id: int


# -------- PAYMENTS --------
class PaymentBase(BaseModel):
    order_id: int
    amount: float
    payment_method: str
    transaction_status: PaymentStatus = PaymentStatus.pending


class PaymentCreate(PaymentBase):
    pass


class PaymentResponse(PaymentBase):
    payment_id: int


# -------- DELIVERY TRACKING --------
class DeliveryTrackingBase(BaseModel):
    order_id: int
    courier_partner: str
    status: DeliveryStatus = DeliveryStatus.shipped
    last_update: datetime = Field(default_factory=datetime.utcnow)


class DeliveryTrackingCreate(DeliveryTrackingBase):
    pass


class DeliveryTrackingResponse(DeliveryTrackingBase):
    tracking_id: int
