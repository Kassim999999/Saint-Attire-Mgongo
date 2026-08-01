from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.database import get_db
from app.dependencies.auth import get_current_admin

from app.models.product import Product
from app.models.order import Order

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("")
def dashboard(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    total_products = db.query(Product).count()

    total_orders = db.query(Order).count()

    pending_orders = (
        db.query(Order)
        .filter(Order.order_status == "Pending")
        .count()
    )

    revenue = (
        db.query(func.sum(Order.total))
        .filter(Order.payment_status == "Paid")
        .scalar()
    ) or 0

    low_stock = (
        db.query(Product)
        .filter(Product.stock <= 5)
        .count()
    )

    return {
        "total_products": total_products,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "revenue": revenue,
        "low_stock": low_stock
    }