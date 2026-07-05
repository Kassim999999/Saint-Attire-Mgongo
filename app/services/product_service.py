from sqlalchemy.orm import Session

from app.models.product import Product

from app.schemas.product import ProductCreate

from app.utils.slug import generate_slug


def create_product(db: Session, product: ProductCreate):

    slug = generate_slug(product.name)

    new_product = Product(
        name=product.name,
        slug=slug,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category=product.category,
        image=product.image,
        image2=product.image2,
    )

    db.add(new_product)

    db.commit()

    db.refresh(new_product)

    return new_product


def get_products(db: Session):

    return db.query(Product).order_by(Product.id.desc()).all()


def get_product(db: Session, product_id: int):

    return db.query(Product).filter(Product.id == product_id).first()


def delete_product(db: Session, product_id: int):

    product = get_product(db, product_id)

    if product:

        db.delete(product)

        db.commit()

    return product