from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    APP_NAME = "SAINT API"
    APP_VERSION = "2.0.0"

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./saint.db"
    )

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "change-this-secret"
    )

    ALGORITHM = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")

    PAYSTACK_PUBLIC_KEY = os.getenv("PAYSTACK_PUBLIC_KEY")

    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")

    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")

    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")

    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")


settings = Settings()