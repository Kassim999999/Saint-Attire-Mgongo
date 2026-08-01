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

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


# Customer places an order
@router.post("", response_model=OrderResponse)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    return order_service.create_order(db, order)


# Admin views all orders
@router.get("", response_model=List[OrderResponse])
def get_orders(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return order_service.get_orders(db)


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