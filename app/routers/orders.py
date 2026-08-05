from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.dependencies.auth import get_current_admin

from app.schemas.order import (
    OrderCreate,
    OrderResponse,
)

from app.services import order_service
from app.schemas.order import OrderStatusUpdate
from app.models.order import Order

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


# Customer places an order
@router.post(
    "",
    summary="Create customer order",
    description="Creates an order from the storefront checkout.",
)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    return order_service.create_order(db, order)


# Admin views all orders
from typing import Optional

@router.get("", response_model=List[OrderResponse])
def get_orders(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Order)

    if status:
        query = query.filter(
            Order.order_status == status
        )

    return query.order_by(
        Order.created_at.desc()
    ).all()


@router.patch(
    "/{order_id}/status",
    summary="Update order status",
    description="Changes the order status to Pending, Processing, Shipped, Delivered or Cancelled.",
)
def update_order_status(
    order_id: int,
    status: OrderStatusUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    valid_statuses = [
        "Pending",
        "Processing",
        "Shipped",
        "Delivered",
        "Cancelled",
    ]

    if status.status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid order status"
        )

    order.order_status = status.status

    db.commit()
    db.refresh(order)

    return {
        "message": "Order status updated",
        "order_status": order.order_status
    }


# Admin views one order
@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    order = order_service.get_order(
        db,
        order_id
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order