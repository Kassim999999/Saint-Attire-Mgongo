from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.dependencies.auth import get_current_admin
from app.models.product import Product
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)
from app.services import product_service

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("", response_model=List[ProductResponse])
def all_products(db: Session = Depends(get_db)):
    return product_service.get_products(db)


@router.get("/{product_id}", response_model=ProductResponse)
def single_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = product_service.get_product(db, product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@router.post("", response_model=ProductResponse)
def create(
    product: ProductCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return product_service.create_product(db, product)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    for key, value in product_data.dict(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted successfully"
    }

from fastapi import UploadFile, File, Form

from app.utils.cloudinary import upload_image


@router.post("/with-images")
def create_product_with_images(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    category_id: int = Form(...),

    image: UploadFile = File(...),
    image2: UploadFile = File(None),

    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    image_url = upload_image(image)

    image2_url = None

    if image2:
        image2_url = upload_image(image2)

    product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        category_id=category_id,
        image=image_url,
        image2=image2_url
    )

    db.add(product)

    db.commit()

    db.refresh(product)

    return product