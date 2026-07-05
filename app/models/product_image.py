from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(
        Integer,
        ForeignKey("products.id")
    )

    image_url = Column(String)

    display_order = Column(Integer, default=1)

    product = relationship(
        "Product",
        back_populates="images"
    )