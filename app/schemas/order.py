from pydantic import BaseModel
from typing import List
from datetime import datetime


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    customer_name: str
    customer_email: str
    customer_phone: str
    shipping_address: str

    items: List[OrderItemCreate]


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int

    customer_name: str
    customer_email: str
    customer_phone: str

    shipping_address: str

    subtotal: float
    delivery_fee: float
    total: float

    payment_status: str
    order_status: str

    created_at: datetime

    items: List[OrderItemResponse]

    class Config:
        from_attributes = True