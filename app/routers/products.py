from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from typing import List

from app.schemas.product import (
    ProductCreate,
    ProductResponse,
)

from app.services import product_service

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=List[ProductResponse])
def all_products(db: Session = Depends(get_db)):
    return product_service.get_products(db)


@router.get("/{product_id}", response_model=ProductResponse)
def single_product(product_id: int, db: Session = Depends(get_db)):

    product = product_service.get_product(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.post("", response_model=ProductResponse)
def create(product: ProductCreate, db: Session = Depends(get_db)):
    return product_service.create_product(db, product)


@router.delete("/{product_id}")
def delete(product_id: int, db: Session = Depends(get_db)):

    product = product_service.delete_product(db, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Deleted"}