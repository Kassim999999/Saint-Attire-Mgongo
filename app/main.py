from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

from app.database.database import Base, engine

from app.routers import auth

from app.database.database import SessionLocal
from app.database.seed import seed_admin

from app.routers.products import router as product_router

from app.routers.categories import router as category_router

from app.routers.auth import router as auth_router

from app.routers import auth

from app.routers.orders import router as order_router

from app.routers.dashboard import router as dashboard_router

from app.routers.uploads import router as upload_router

from app.routers.payments import router as payment_router

from app.routers.webhooks import router as webhook_router

from fastapi.staticfiles import StaticFiles

import app.models

Base.metadata.create_all(bind=engine)

db = SessionLocal()

seed_admin(db)

db.close()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

app.include_router(auth.router)

app.include_router(product_router)

app.include_router(category_router)

app.include_router(auth_router)

app.include_router(order_router)

app.include_router(dashboard_router)

app.include_router(upload_router)

app.include_router(payment_router)

app.include_router(webhook_router)



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to SAINT API",
        "version": settings.APP_VERSION
    }