from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

from app.database.database import Base, engine

from app.routers import auth

from app.database.database import SessionLocal
from app.database.seed import seed_admin

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



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Welcome to SAINT API",
        "version": settings.APP_VERSION
    }