from pydantic import BaseModel
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    image: Optional[str] = None
    image2: Optional[str] = None
    category_id: Optional[int] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    image: Optional[str] = None
    image2: Optional[str] = None
    category_id: Optional[int] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int
    image: Optional[str]
    image2: Optional[str]
    category_id: Optional[int]

    class Config:
        from_attributes = True