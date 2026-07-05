from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.admin import Admin
from app.schemas.admin import AdminLogin
from app.core.security import (
    verify_password,
    create_access_token,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/admin/login")
def admin_login(
    admin: AdminLogin,
    db: Session = Depends(get_db)
):

    existing_admin = (
        db.query(Admin)
        .filter(Admin.username == admin.username)
        .first()
    )

    if not existing_admin:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        admin.password,
        existing_admin.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
        {"sub": existing_admin.username}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }