from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.database import Base


class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)

    description = Column(String)

    banner_image = Column(String)

    is_live = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    products = relationship(
        "Product",
        back_populates="collection",
        cascade="all, delete"
    )