from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate
from app.utils.slug import generate_slug


def create_category(db: Session, category: CategoryCreate):
    new_category = Category(
        name=category.name,
        slug=generate_slug(category.name)
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


def get_categories(db: Session):
    return db.query(Category).order_by(Category.id.desc()).all()


def get_category(db: Session, category_id: int):
    return db.query(Category).filter(
        Category.id == category_id
    ).first()