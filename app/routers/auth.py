from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.admin import Admin
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
)
from app.utils.security import create_access_token
from app.utils.hash import verify_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    admin = db.query(Admin).filter(
        Admin.email == credentials.email
    ).first()

    if not admin:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        credentials.password,
        admin.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
        {
            "sub": str(admin.id),
            "email": admin.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }