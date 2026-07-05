from typing import Optional

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category: Optional[str] = None
    image: Optional[str] = None
    image2: Optional[str] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category: Optional[str] = None
    image: Optional[str] = None
    image2: Optional[str] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: str
    price: float
    stock: int
    category: Optional[str] = None
    image: Optional[str] = None
    image2: Optional[str] = None

    class Config:
        orm_mode = True