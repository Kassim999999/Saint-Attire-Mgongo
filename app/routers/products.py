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
    ProductListResponse,
    StockUpdate,
)
from app.services import product_service
from typing import Optional
from sqlalchemy import asc, desc

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)




@router.get(
    "",
    response_model=ProductListResponse,
    summary="Get all products",
    description="""
Retrieve products with optional:

- Search
- Category filter
- Price filter
- Sorting
- Pagination
""",
)
def all_products(
    search: Optional[str] = None,
    category: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort: Optional[str] = None,
    page: int = 1,
    limit: int = 12,
    db: Session = Depends(get_db),
):
    query = db.query(Product)

    # Search
    if search:
        query = query.filter(
            Product.name.ilike(f"%{search}%")
        )

    # Category
    if category:
        query = query.filter(
            Product.category_id == category
        )

    # Minimum price
    if min_price is not None:
        query = query.filter(
            Product.price >= min_price
        )

    # Maximum price
    if max_price is not None:
        query = query.filter(
            Product.price <= max_price
        )

    # Sorting
    if sort == "price_asc":
        query = query.order_by(
            asc(Product.price)
        )

    elif sort == "price_desc":
        query = query.order_by(
            desc(Product.price)
        )

    elif sort == "newest":
        query = query.order_by(
            desc(Product.created_at)
        )

    elif sort == "oldest":
        query = query.order_by(
            asc(Product.created_at)
        )

    # Pagination
    offset = (page - 1) * limit

    total_products = query.count()

    products = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    total_pages = (
        total_products + limit - 1
    ) // limit

    return {
        "page": page,
        "limit": limit,
        "total_products": total_products,
        "total_pages": total_pages,
        "products": products,
    }


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Get one product",
    description="Returns a single product by its ID.",
)
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


@router.post(
    "",
    response_model=ProductResponse,
    summary="Create a product",
    description="Creates a new product. Admin authentication required.",
)
def create(
    product: ProductCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return product_service.create_product(db, product)


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Update product",
    description="Updates an existing product.",
)
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


@router.delete(
    "/{product_id}",
    summary="Delete product",
    description="Deletes a product permanently.",
)
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


@router.post(
    "/with-images",
    summary="Create product with Cloudinary images",
    description="Uploads one or two images to Cloudinary and creates the product.",
)
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


@router.patch("/{product_id}/restock")
def restock_product(
    product_id: int,
    stock: StockUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
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

    product.stock += stock.quantity

    db.commit()
    db.refresh(product)

    return {
        "message": "Product restocked successfully",
        "current_stock": product.stock
    }


@router.patch("/{product_id}/stock")
def update_stock(
    product_id: int,
    stock: StockUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
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

    product.stock = stock.quantity

    db.commit()
    db.refresh(product)

    return {
        "message": "Stock updated successfully",
        "current_stock": product.stock
    }