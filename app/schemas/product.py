from pydantic import BaseModel, Field
from typing import Optional


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)

    description: str = Field(..., min_length=5)

    price: float = Field(..., gt=0)

    stock: int = Field(..., ge=0)

    category_id: Optional[int] = None

    image: Optional[str] = None

    image2: Optional[str] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)

    description: Optional[str] = Field(None, min_length=5)

    price: Optional[float] = Field(None, gt=0)

    stock: Optional[int] = Field(None, ge=0)

    category_id: Optional[int] = None

    image: Optional[str] = None

    image2: Optional[str] = None


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


from typing import List

class ProductListResponse(BaseModel):
    page: int
    limit: int
    total_products: int
    total_pages: int
    products: List[ProductResponse]


class StockUpdate(BaseModel):
    quantity: int = Field(..., ge=0)