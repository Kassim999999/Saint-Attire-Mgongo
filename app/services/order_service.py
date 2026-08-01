from sqlalchemy.orm import Session

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product

from app.schemas.order import OrderCreate


DELIVERY_FEE = 300


def create_order(db: Session, order: OrderCreate):

    subtotal = 0

    order_items = []

    # Validate products and calculate subtotal
    for item in order.items:

        product = (
            db.query(Product)
            .filter(Product.id == item.product_id)
            .first()
        )

        if not product:
            raise Exception(
                f"Product {item.product_id} not found"
            )

        if product.stock < item.quantity:
            raise Exception(
                f"{product.name} is out of stock"
            )

        subtotal += product.price * item.quantity

        order_items.append({
            "product": product,
            "quantity": item.quantity,
            "price": product.price
        })

    total = subtotal + DELIVERY_FEE

    new_order = Order(
        customer_name=order.customer_name,
        customer_email=order.customer_email,
        customer_phone=order.customer_phone,
        shipping_address=order.shipping_address,

        subtotal=subtotal,
        delivery_fee=DELIVERY_FEE,
        total=total,
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Save order items
    for item in order_items:

        db_item = OrderItem(
            order_id=new_order.id,
            product_id=item["product"].id,
            quantity=item["quantity"],
            price=item["price"],
        )

        db.add(db_item)

        # Reduce stock
        item["product"].stock -= item["quantity"]

    db.commit()
    db.refresh(new_order)

    return new_order


def get_orders(db: Session):
    return (
        db.query(Order)
        .order_by(Order.id.desc())
        .all()
    )


def get_order(db: Session, order_id: int):
    return (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )