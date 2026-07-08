from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    description = Column(String, nullable=False)

    price = Column(Float, nullable=False)

    image = Column(String)

    image2 = Column(String)

    stock = Column(Integer, default=0)

    category_id = Column(
        Integer,
        ForeignKey("categories.id")
    )

    category = relationship(
        "Category",
        back_populates="products"
    )

    images = relationship(
    "ProductImage",
    back_populates="product",
    cascade="all, delete-orphan"
)

    sizes = relationship(
    "ProductSize",
    back_populates="product",
    cascade="all, delete-orphan"
)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )