from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    customer_name = Column(String, nullable=False)

    customer_email = Column(String, nullable=False)

    customer_phone = Column(String, nullable=False)

    shipping_address = Column(String, nullable=False)

    subtotal = Column(Float, nullable=False)

    delivery_fee = Column(Float, default=0)

    total = Column(Float, nullable=False)

    payment_status = Column(
        String,
        default="Pending"
    )

    payment_reference = Column(
    String,
    nullable=True
)

    order_status = Column(
        String,
        default="Pending"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )