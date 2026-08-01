import requests

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.core.config import settings
from app.models.order import Order

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post("/initialize/{order_id}")
def initialize_payment(
    order_id: int,
    db: Session = Depends(get_db)
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
    
    if order.total <= 0:
     raise HTTPException(
        status_code=400,
        detail="Invalid order total"
    )

    amount = int(order.total)

    payload = {
        "email": order.customer_email,
        "amount": amount * 100,
        "reference": f"SAINT-{order.id}"
    }

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api.paystack.co/transaction/initialize",
        json=payload,
        headers=headers
    )

    data = response.json()

    if not data["status"]:
        raise HTTPException(
            status_code=400,
            detail=data["message"]
        )

    order.payment_reference = data["data"]["reference"]
    db.commit()

    return data["data"]

@router.get("/verify/{reference}")
def verify_payment(
    reference: str,
    db: Session = Depends(get_db)
):
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }

    response = requests.get(
        f"https://api.paystack.co/transaction/verify/{reference}",
        headers=headers
    )

    data = response.json()

    if not data["status"]:
        raise HTTPException(
            status_code=400,
            detail="Verification failed"
        )

    if data["data"]["status"] == "success":
        order = (
            db.query(Order)
            .filter(Order.payment_reference == reference)
            .first()
        )

        if order:
            order.payment_status = "Paid"
            db.commit()

    return data["data"]