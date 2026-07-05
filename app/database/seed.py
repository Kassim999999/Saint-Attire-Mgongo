from sqlalchemy.orm import Session

from app.models.admin import Admin
from app.core.security import hash_password


def seed_admin(db: Session):

    admin = (
        db.query(Admin)
        .filter(Admin.username == "admin")
        .first()
    )

    if admin:
        print("✅ Admin already exists")
        return

    new_admin = Admin(
        username="admin",
        email="admin@saintattire.com",
        password=hash_password("saint2026")
    )

    db.add(new_admin)
    db.commit()

    print("✅ Default admin created")