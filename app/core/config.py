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

    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")

    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


settings = Settings()