from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    slug: str


class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str

    class Config:
        from_attributes = True