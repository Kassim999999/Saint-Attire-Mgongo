from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class ProductSize(Base):
    __tablename__ = "product_sizes"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(
        Integer,
        ForeignKey("products.id")
    )

    size = Column(String(10))

    stock = Column(Integer, default=0)

    product = relationship(
        "Product",
        back_populates="sizes"
    )