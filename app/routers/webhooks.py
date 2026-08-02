import hashlib
import hmac

from fastapi import APIRouter, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.database import SessionLocal
from app.models.order import Order

router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"]
)


@router.post("/paystack")
async def paystack_webhook(request: Request):

    signature = request.headers.get("x-paystack-signature")

    body = await request.body()

    expected_signature = hmac.new(
        settings.PAYSTACK_SECRET_KEY.encode(),
        body,
        hashlib.sha512
    ).hexdigest()

    if signature != expected_signature:
        raise HTTPException(
            status_code=401,
            detail="Invalid signature"
        )

    event = await request.json()

    if event["event"] != "charge.success":
        return {"status": "ignored"}

    reference = event["data"]["reference"]

    db: Session = SessionLocal()

    try:

        order = (
            db.query(Order)
            .filter(Order.payment_reference == reference)
            .first()
        )

        if not order:
            return {"status": "order_not_found"}

        # Prevent duplicate webhook processing
        if order.payment_status == "Paid":
            return {"status": "already_processed"}

        order.payment_status = "Paid"
        order.order_status = "Processing"

        for item in order.items:

            product = item.product

            if product:

                product.stock -= item.quantity

                if product.stock < 0:
                    product.stock = 0

        db.commit()

    finally:
        db.close()

    return {
        "status": "success"
    }