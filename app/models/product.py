from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    ForeignKey,
    DateTime
)

from sqlalchemy.orm import relationship

from datetime import datetime

from app.database.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    category_id = Column(
        Integer,
        ForeignKey("categories.id")
    )

    collection_id = Column(
        Integer,
        ForeignKey("collections.id")
    )

    name = Column(String(200), nullable=False)

    slug = Column(String(200), unique=True)

    description = Column(String)

    price = Column(Float)

    featured = Column(Boolean, default=False)

    active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    category = relationship(
        "Category",
        back_populates="products"
    )

    collection = relationship(
        "Collection",
        back_populates="products"
    )

    images = relationship(
        "ProductImage",
        back_populates="product",
        cascade="all, delete"
    )

    sizes = relationship(
        "ProductSize",
        back_populates="product",
        cascade="all, delete"
    )